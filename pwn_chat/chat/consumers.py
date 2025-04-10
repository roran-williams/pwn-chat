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
        message = data['message']
        username = data['username']

        # Broadcast the message to the group
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message,
                'username': username
            }
        )

    # async def save_to_db(self,data):
    #     # Save the message to the database
    #     user = await sync_to_async(User.objects.get)(username='pwn')
    #     await sync_to_async(Message.objects.create)(
    #         user=user,
    #         text='message',
    #         timestamp=datetime.date.today
    #         # room_name=self.room_name  # Save room name
    #     )

    async def chat_message(self, event):
        username=event['username']
        message = event['message']
        user = await sync_to_async(User.objects.get)(username=username)
        await sync_to_async(Message.objects.create)(
            user=user,
            text=message,
            timestamp=datetime.date.today
            # room_name=self.room_name  # Save room name
        )
        await self.send(text_data=json.dumps({
            'message': event['message'],
            'username': event['username']
        }))

    
    