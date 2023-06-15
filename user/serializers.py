from rest_framework import serializers
from django.contrib.auth.models import User

from sociobackend.utils import time_formating
from .models import *
from rest_framework_simplejwt.tokens import RefreshToken


class UserSerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField(read_only=True)
    _id = serializers.SerializerMethodField(read_only=True)
    isAdmin = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = User
        fields = ['id', '_id', 'username', 'email', 'name', 'isAdmin']

    def get_name(self, obj):
        name = obj.first_name
        if name == '':
            name = obj.email
        return name
    
    def get__id (self, obj):
        return obj.id
    
    def get_isAdmin (self, obj):
        return obj.is_staff
    

class UserSerializerWithToken(UserSerializer):
    token = serializers.SerializerMethodField(read_only=True)
    userProfile = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = User
        fields = ['id', '_id', 'username', 'email', 'name', 'isAdmin', 'token', 'userProfile']

    def get_token(self, obj):
        token = RefreshToken.for_user(obj)
        return  str(token.access_token)
    
    def get_userProfile(self, obj):
        user_profile = UserProfile.objects.get(user = obj)
        serializer = UserProfileSerializer(user_profile, many=False)
        return {
                'profilePic':serializer.data['profilePic'],
                'username':serializer.data['username'],
                'name':serializer.data['name'],
        }


class UserProfileSerializer(serializers.ModelSerializer):
    is_following = serializers.SerializerMethodField(read_only=True)
    following_count = serializers.SerializerMethodField(read_only=True)
    followers = UserSerializer(read_only=True, many=True)
    user = UserSerializer(read_only=True, many=False)


    class Meta:
        model = UserProfile
        fields = ['id', 'user', 'name', 'username', 'profilePic', 'bio', 'followers_count', 'followers', 'is_following', 'following_count']      
        # fields = '__all__'     

    def get_following_count(self, obj):
        following_count = obj.user.following.count()
        return following_count
    def get_is_following(self, obj):
        return True


class UserProfileSerializerWithLessDetails(UserProfileSerializer):
    user = UserSerializer(read_only=True, many=False)

    class Meta:
        model = UserProfile
        fields = ['id', 'user', 'name', 'username', 'profilePic']      



