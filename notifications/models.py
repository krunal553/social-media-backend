# modles.py
import json
import time
import uuid
from django.db import models
from django.contrib.auth.models import User
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync

from user.serializers import UserProfileSerializerWithLessDetails


# from .serializers import NotificationSerializer

class Notification(models.Model):
    id = models.UUIDField(default=uuid.uuid4,  unique=True, primary_key=True, editable=False)
    created_by = models.ForeignKey(User,on_delete=models.CASCADE, null=True, blank=True)
    to_user = models.ForeignKey(User,on_delete=models.CASCADE, null=True, blank=True, related_name='notifications')
    created_at = models.DateTimeField(auto_now_add=True)
    message = models.CharField(max_length=255)
    is_seen = models.BooleanField(default=False)


    def __str__(self):
        return self.created_by.username +' '+ self.message +' '+ self.to_user.username

    async def notification_group_send(self, event):
        data = json.loads(event['value'])
        await self.channel_layer.group_send(self.room_group_name, {
            'type': 'send_notifications',
            'value': json.dumps(data)
        })

    def save(self, *args, **kwars):
        channel_layer = get_channel_layer()
        notification_objs = Notification.objects.filter(is_seen=False).count()
        data = {
            # 'to_user': self.to_user,
            'count': notification_objs, 
            'to_user': UserProfileSerializerWithLessDetails(self.to_user.userprofile, many=False).data,
            'created_by': UserProfileSerializerWithLessDetails(self.created_by.userprofile, many=False).data,
            'message': self.created_by.username+' ' +self.message,
            
            "is_seen": self.is_seen,
        }

        # serializer = NotificationSerializer(notification_objs, many=True)

        async_to_sync(channel_layer.group_send)(
            'new_consumer_group',{
                'type': 'notification_group_send',
                'value': json.dumps(data)
            }

        )
        super(Notification, self).save(*args, **kwars)