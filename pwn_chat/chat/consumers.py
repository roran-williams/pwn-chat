import json
from channels.generic.websocket import AsyncWebsocketConsumer
from asgiref.sync import sync_to_async
import datetime
from django.contrib.auth.models import User
from .models import Message

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_group_name = "chatroom"

        # Join the chat room
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        # Leave the chat room
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        data = json.loads(text_data)
        message = data.get('message')  # Use .get() to avoid KeyError
        username = data.get('username')

        if not message or not username:
            await self.send(text_data=json.dumps({
                'error': 'Message and username are required'
            }))
            return

        # Broadcast the message to the group
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message,
                'username': username
            }
        )

    async def chat_message(self, event):
        username = event['username']
        message = event['message']
        
        try:
            user = await sync_to_async(User.objects.get)(username=username)
            
            # Save the message to the database with timestamp including time
            timestamp = datetime.datetime.now().strftime('%Y-%m-%dT%H:%M:%SZ')  # ISO 8601 format

            # Save message
            await sync_to_async(Message.objects.create)(
                user=user,
                text=message,
                timestamp=timestamp  # Save in the desired format
            )
            
            # Send message with timestamp to the frontend
            await self.send(text_data=json.dumps({
                'message': message,
                'username': username,
                'timestamp': timestamp
            }))
        except User.DoesNotExist:
            # Handle case where the user doesn't exist
            await self.send(text_data=json.dumps({
                'error': 'User not found'
            }))
