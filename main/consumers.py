import json
from channels.generic.websocket import AsyncWebsocketConsumer
from main.models import Message, Room
from channels.db import database_sync_to_async


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = self.room_name

        # Join room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        await self.accept()

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    # Receive message from WebSocket
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        user = self.scope['user']

        # Send message to room group
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message,
                'user': user.username
            }
        )

    # Receive message from room group
    async def chat_message(self, event):
        user = event['user']
        message = event['message']

        # Create messages
        await self.create_message(message)

        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'message': message,
            'user': user
        }))

    @database_sync_to_async
    def create_message(self, content):
        room = Room.objects.get(room=self.room_name)
        user = self.scope['user']
        message = Message.objects.create(
            user = user,
            content = content,
            room = room
        )
