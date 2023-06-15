from rest_framework import serializers
from django.contrib.auth.models import User

from sociobackend.utils import time_formating
from .models import Post, PostComment
from user.models import UserProfile
from user.serializers import UserProfileSerializer, UserSerializer
from rest_framework_simplejwt.tokens import RefreshToken

class CreatePostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        # fields = ['desc', 'user', 'image']
        fields = '__all__'

class PostSerializer(serializers.ModelSerializer):
    likers = UserSerializer(read_only=True, many=True)
    comments_count = serializers.SerializerMethodField(read_only=True)
    user_details = serializers.SerializerMethodField(read_only=True)
    timestamp = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Post
        fields = ['_id', 'likers','desc', 'image', 'likes_count', 'user', 'comments_count', 'user_details', 'timestamp']


    # def get_profilePic(self, obj):
    #     user_of_post = User.objects.get(username= obj.user.username)
    #     user_profile = UserProfile.objects.get(user = user_of_post)
    #     serializer = UserProfileSerializer(user_profile, many=False)
    #     return serializer.data['profilePic']
    
    def get_user_details(self, obj):
        # user_of_comment = User.objects.get(id= obj.user)
        # user_profile = UserProfile.objects.get(user = obj.user)
        try:
            user_profile = UserProfile.objects.get(user = obj.user)
            serializer = UserProfileSerializer(user_profile, many=False)
            return {
                    'profilePic':serializer.data['profilePic'],
                    'username':serializer.data['username'],
                    'name':serializer.data['name'],
                    'user':serializer.data['user'],
            }
        except:
            pass
        
    
    def get_comments_count(self, obj):
        return PostComment.objects.filter(post_id=obj._id).count()

    def get_timestamp (self, obj):
        return time_formating(input_time=obj.timestamp)


class PostCommentSerializer(serializers.ModelSerializer):
    # user = UserSerializer(read_only=True, many=False)
    profilePic = serializers.SerializerMethodField(read_only=True)
    user_details = serializers.SerializerMethodField(read_only=True)
    commented_on = serializers.SerializerMethodField(read_only=True)


    class Meta:
        model = PostComment
        fields = ['id', 'comment_text', 'commented_on', 'user', 'post_id', 'profilePic', 'user_details']

    def get_profilePic(self, obj):
        # user_of_comment = User.objects.get(id= obj.user)
        user_profile = UserProfile.objects.get(user = obj.user)
        serializer = UserProfileSerializer(user_profile, many=False)
        return serializer.data['profilePic']

    def get_user_details(self, obj):
        # user_of_comment = User.objects.get(id= obj.user)
        user_profile = UserProfile.objects.get(user = obj.user)
        serializer = UserProfileSerializer(user_profile, many=False)
        return {
                'profilePic':serializer.data['profilePic'],
                'username':serializer.data['username'],
                'name':serializer.data['name'],
                'user':serializer.data['user'],
        }
    
    def get_commented_on(self, obj):
        return time_formating(input_time=obj.commented_on)

    
    