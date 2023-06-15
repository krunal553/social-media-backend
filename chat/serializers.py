import json
from rest_framework import serializers
from .models import UserMessage, Thread
from user.serializers import UserProfileSerializerWithLessDetails
from django.contrib.auth.models import User
from user.models import UserProfile
from sociobackend.utils import time_formating


class MessageSerializer(serializers.ModelSerializer):
    sender = UserProfileSerializerWithLessDetails(read_only=True)

    class Meta:
        model = UserMessage
        fields = '__all__'


class ThreadSerializer(serializers.ModelSerializer):
    chat_messages = serializers.SerializerMethodField(read_only=True)
    last_message = serializers.SerializerMethodField(read_only=True)
    un_seen_count = serializers.SerializerMethodField(read_only=True)
    users = UserProfileSerializerWithLessDetails(many=True, read_only=True)
    timestamp = serializers.SerializerMethodField(read_only=True)


    class Meta:
        model = Thread
        fields = ['thread_id', 'updated', 'timestamp', 'users', 'is_one_to_one', 'chat_messages', 'last_message',
                  'un_seen_count']

    def get_chat_messages(self, obj):
        messages = MessageSerializer(obj.messages.order_by('timestamp'), many=True)
        return messages.data

    def get_last_message(self, obj):
        serializer = MessageSerializer(obj.messages.order_by('timestamp').last(), many=False)
        return serializer.data

    def get_un_seen_count(self, obj):
        messages = obj.messages.filter(is_seen=False).count()
        return messages

    def get_timestamp(self, obj):
        return time_formating(input_time=obj.timestamp)


class ThreadSerializerForChatList(serializers.ModelSerializer):
    chat_messages = serializers.SerializerMethodField(read_only=True)
    last_message = serializers.SerializerMethodField(read_only=True)
    un_seen_count = serializers.SerializerMethodField(read_only=True)
    user_to_chat_with = serializers.SerializerMethodField()
    users = UserProfileSerializerWithLessDetails(many=True, read_only=True)
    timestamp = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Thread
        fields = ['thread_id', 'updated', 'timestamp', 'users', 'user_to_chat_with', 'is_one_to_one', 'chat_messages', 'last_message',
                  'un_seen_count']

    def get_chat_messages(self, obj):
        messages = MessageSerializer(obj.messages.order_by('timestamp'), many=True)
        return messages.data

    def get_last_message(self, obj):
        serializer = MessageSerializer(obj.messages.order_by('timestamp').last(), many=False)
        return serializer.data

    def get_un_seen_count(self, obj):
        messages = obj.messages.filter(is_seen=False).count()
        return messages

    def get_user_to_chat_with(self, obj):
        # data = obj.users.filter()
        # name = data[0]['users'][0]['username']
        user = self.context['request'].user
        user_prof = obj.users.exclude(username=user.username).first()
        data = UserProfileSerializerWithLessDetails(user_prof, many=False)
        

        return data.data
        # except:
        #     return json.dumps(obj.users)

    def get_timestamp(self, obj):
        return time_formating(input_time=obj.timestamp)
