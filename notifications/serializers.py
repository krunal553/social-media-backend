from rest_framework import serializers
from .models import Notification
from user.serializers import UserProfileSerializerWithLessDetails
from sociobackend.utils import time_formating

class NotificationSerializer(serializers.ModelSerializer):
    created_by = serializers.SerializerMethodField(read_only=True)
    created_at = serializers.SerializerMethodField(read_only=True)


    class Meta:
        model = Notification
        fields = ( 'id', 'created_by', 'to_user', 'created_at', 'message', 'is_seen')

    def get_created_by(self, obj):
        return UserProfileSerializerWithLessDetails(obj.created_by.userprofile, many=False).data

        
    def get_created_at(self, obj):
        return time_formating(input_time=obj.created_at)
        