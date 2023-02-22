import json
from channels.generic.websocket import AsyncWebsocketConsumer
from asgiref.sync import sync_to_async
from django.utils import timezone
from .models import Room, RoomMessage
from core.models import User


class RoomConsumer(AsyncWebsocketConsumer):

    async def connect(self):
        self.user = self.scope['user']
        self.id = self.scope['url_route']['kwargs']['room_id']
        self.room_group_name = f'room_{self.id}'
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
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        room_id = text_data_json['room_id']
        user = text_data_json['user']

        await self.save_message(user, room_id, message)

        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'room_message',
                'message': message,
                'room_id': room_id,
                'user': user,
                'datetime': timezone.now().isoformat(),
            }
        )

    async def room_message(self, event):
        await self.send(text_data=json.dumps(event))

    @sync_to_async
    def save_message(self, user, room_id, message):
        sender = User.objects.get(id=user['id'])
        room = Room.objects.get(id=room_id)

        RoomMessage.objects.create(user=sender, room=room, content=message)

