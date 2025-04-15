import json
import re
from channels.generic.websocket import AsyncWebsocketConsumer
from asgiref.sync import sync_to_async
from django.contrib.auth.models import User
from .models import PrivateMessage
from django.utils import timezone

class PrivateChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.user = self.scope['user']
        self.other_username = self.scope['url_route']['kwargs']['username']

        # Reject connection if user is not authenticated
        if not self.user.is_authenticated:
            await self.close()
            return

        # Get the other user object
        self.other_user = await sync_to_async(User.objects.get)(username=self.other_username)

        # Sanitize usernames
        def clean_username(username):
            return re.sub(r'[^a-zA-Z0-9_.-]', '_', username)

        cleaned_user = clean_username(self.user.username)
        cleaned_other = clean_username(self.other_username)

        # Sort usernames to ensure both users get the same group name
        usernames = sorted([cleaned_user, cleaned_other])
        self.room_group_name = f"private_{usernames[0]}_{usernames[1]}"

        # Join group
        await self.channel_layer.group_add(self.room_group_name, self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    async def receive(self, text_data):
        data = json.loads(text_data)
        message = data['message']

        # Save the message in the database
        await sync_to_async(PrivateMessage.objects.create)(
            sender=self.user,
            receiver=self.other_user,
            text=message
        )

        timestamp = timezone.now().isoformat()

        # Send message to group
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message,
                'sender': self.user.username,
                'timestamp': timestamp
            }
        )

    async def chat_message(self, event):
        # Send the message to WebSocket
        await self.send(text_data=json.dumps({
            'message': event['message'],
            'sender': event['sender'],
            'timestamp': event['timestamp']
        }))
