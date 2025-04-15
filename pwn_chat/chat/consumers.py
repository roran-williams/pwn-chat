import json
from channels.generic.websocket import AsyncWebsocketConsumer
from asgiref.sync import sync_to_async
from django.contrib.auth.models import User
from .models import Message, Room
from django.utils import timezone
import re


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = f"chat_{self.room_name}"

        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

    
    async def disconnect(self, close_code):
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
            sender = await sync_to_async(User.objects.get)(username=username)
            
            room = await sync_to_async(Room.objects.get_or_create)(name=self.room_name)
            
            # Save the message to the database with timestamp including time
            timestamp = timezone.now().isoformat()

            # Save message
            await sync_to_async(Message.objects.create)(
                
                room=room[0],
                text=message,
                sender=sender,
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


# class PrivateChatConsumer(AsyncWebsocketConsumer):
#     async def connect(self):
#         print('00000000000000000000000')

#         self.me = self.scope['user'].username
#         self.other_user = self.scope['url_route']['kwargs']['username']
        
#         self.room_name = f"private_{min(self.me, self.other_user)}_{max(self.me, self.other_user)}"

#         await self.channel_layer.group_add(
#             self.room_name,
#             self.channel_name
#         )
#         await self.accept()

    
#     async def disconnect(self, close_code):
#         await self.channel_layer.group_discard(
#             self.room_name,
#             self.channel_name
#         )

#     async def receive(self, text_data):
#         data = json.loads(text_data)
        
#         message = data['message']
#         sender = await sync_to_async(User.objects.get)(username=self.me)
#         receiver = await sync_to_async(User.objects.get)(username=self.other_user)
        
#         msg = await sync_to_async(Message.objects.create)(
#             sender=sender, receiver=receiver, text=message
#         )

#         await self.channel_layer.group_send(
#             self.room_name,
#             {
#                 'type': 'chat_message',
#                 'message': message,
#                 'sender': self.me
#             }
#         )

#     async def chat_message(self, event):
#         await self.send(text_data=json.dumps({
#             'message': event['message'],
#             'sender': event['sender']
#         }))

# import json
# from channels.generic.websocket import AsyncWebsocketConsumer
# from asgiref.sync import sync_to_async
# from django.contrib.auth.models import User
# from .models import PrivateMessage
# from django.utils import timezone

# class PrivateChatConsumer(AsyncWebsocketConsumer):
#     async def connect(self):
        

#         self.user = self.scope['user']
#         self.other_username = self.scope['url_route']['kwargs']['username']
        
#         if not self.user.is_authenticated:
#             await self.close()
#             return
        
#         self.other_user = await sync_to_async(User.objects.get)(username=self.other_username)
#         def clean_username(username):
#             return re.sub(r'[^a-zA-Z0-9_.-]', '_', username)

#         cleaned_user = clean_username(self.scope['user'].username)
#         cleaned_other = clean_username(self.other_username)

        
#         # self.room_group_name = f"private_{min(self.user.username, self.other_user.username)}_{max(self.user.username, self.other_user.username)}"
#         self.room_group_name = f"private_{cleaned_user}_{cleaned_other}"

#         await self.channel_layer.group_add(self.room_group_name, self.channel_name)
#         await self.accept()

    
#     async def disconnect(self, close_code):
#         await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

#     async def receive(self, text_data):
#         data = json.loads(text_data)
#         message = data['message']

#         msg = await sync_to_async(PrivateMessage.objects.create)(
#             sender=self.user, receiver=self.other_user, text=message
#         )

#         timestamp = timezone.now().isoformat()

#         await self.channel_layer.group_send(
#             self.room_group_name,
#             {
#                 'type': 'chat_message',
#                 'message': message,
#                 'sender': self.user.username,
#                 'timestamp': timestamp
#             }
#         )

#     async def chat_message(self, event):
#         await self.send(text_data=json.dumps({
#             'message': event['message'],
#             'sender': event['sender'],
#             'timestamp': event['timestamp']
#         }))




# import json
# import re
# from channels.generic.websocket import AsyncWebsocketConsumer
# from asgiref.sync import sync_to_async
# from django.contrib.auth.models import User
# from .models import PrivateMessage
# from django.utils import timezone

# class PrivateChatConsumer(AsyncWebsocketConsumer):
#     async def connect(self):
#         self.user = self.scope['user']
#         self.other_username = self.scope['url_route']['kwargs']['username']

#         # Reject connection if user is not authenticated
#         if not self.user.is_authenticated:
#             await self.close()
#             return

#         # Get the other user object
#         self.other_user = await sync_to_async(User.objects.get)(username=self.other_username)

#         # Sanitize usernames
#         def clean_username(username):
#             return re.sub(r'[^a-zA-Z0-9_.-]', '_', username)

#         cleaned_user = clean_username(self.user.username)
#         cleaned_other = clean_username(self.other_username)

#         # Sort usernames to ensure both users get the same group name
#         usernames = sorted([cleaned_user, cleaned_other])
#         self.room_group_name = f"private_{usernames[0]}_{usernames[1]}"

#         # Join group
#         await self.channel_layer.group_add(self.room_group_name, self.channel_name)
#         await self.accept()

#     async def disconnect(self, close_code):
#         await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

#     async def receive(self, text_data):
#         data = json.loads(text_data)
#         message = data['message']

#         # Save the message in the database
#         await sync_to_async(PrivateMessage.objects.create)(
#             sender=self.user,
#             receiver=self.other_user,
#             text=message
#         )

#         timestamp = timezone.now().isoformat()

#         # Send message to group
#         await self.channel_layer.group_send(
#             self.room_group_name,
#             {
#                 'type': 'chat_message',
#                 'message': message,
#                 'sender': self.user.username,
#                 'timestamp': timestamp
#             }
#         )

#     async def chat_message(self, event):
#         # Send the message to WebSocket
#         await self.send(text_data=json.dumps({
#             'message': event['message'],
#             'sender': event['sender'],
#             'timestamp': event['timestamp']
#         }))
