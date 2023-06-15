# consumers.py 
    
import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.generic.websocket import AsyncJsonWebsocketConsumer



class NotificationsConsumer(AsyncJsonWebsocketConsumer):
    async def connect(self):
        self.room_name = "new_consumer"
        self.room_group_name = "new_consumer_group"

        await (self.channel_layer.group_add)(
                    self.room_group_name,
                    self.channel_name
        )
        await self.accept()
        await self.send(text_data=json.dumps({'payload': {'message': 'connected from new async json consumer'}}))

    async def receive(self, text_data):
        print(text_data)
        print('receive called')

        await self.send(text_data=json.dumps({'status': 'we got you'}))

        pass

    async def disconnect(self, *args, **kwargs):
        # await self.channel_layer.group_discard(
        #     self.room_group_name,
        #     self.channel_name
        # )
        print('disconnected')

    async def send_notifications(self, event):
        # data = json.loads(event.get('value'))
        # await self.send(text_data=json.dumps({'payload': data}))
        print ('send notification')
        print (event.get('value'))
        data = json.loads(event.get('value'))
        await self.send(text_data=json.dumps({'payload': data}))
        print ('send notification')

    async def notification_group_send(self, event):
        data = json.loads(event['value'])
        await self.channel_layer.group_send(self.room_group_name, {
            'type': 'send_notifications',
            'value': json.dumps(data)
        })