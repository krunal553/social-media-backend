import json
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
from channels.generic.websocket import AsyncWebsocketConsumer

from .models import Thread, UserMessage
from .serializers import MessageSerializer

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.thread_id = self.scope['url_route']['kwargs']['thread_id']
        # self.thread_id = '553'
        self.room_group_name = 'chat_%s' % self.thread_id

        # Join room group
        await (self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        # Leave room group
        await (self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name
        )

    # Receive message from WebSocket
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        # message = text_data_json['message']
        # timestamp = text_data_json['timestamp']
        # senderName = text_data_json['senderName']
        # id = text_data_json['id']

        # Save message to database
        # thread = Thread.objects.get(id=self.thread_id)
        # sender = self.scope["user"].userprofile
        # user_message = UserMessage.objects.create(thread=thread, sender=sender, body=message)
        # user_message.save()

        # Send message to room group
        await (self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type': 'chat_message',
                # 'message': MessageSerializer(user_message).data
                'message': "new msg"
                # 'message': {
                #     "message": message,
                #     "timestamp": timestamp,
                #     'senderName': senderName,
                #     'id': id,
                # },
            }
        )

    # Receive message from room group
    async def chat_message(self, event):
        message = event['message']

        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'message': message
        }))


