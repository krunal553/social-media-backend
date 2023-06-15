from django.db import models

from django.contrib.auth.models import User

from django.utils import timezone


import os

from uuid import uuid4
from datetime import date


def path_and_rename(instance, filename):
    upload_to=''
    ext=filename.split('.')[-1]
    filename ='{}.{}'.format("IMG"+date.today().strftime("%d%m%Y")+uuid4().hex, ext)

    return os.path.join(upload_to, filename)

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='userprofile', default=None, null=True)
    name = models.CharField(max_length=200, null=True)
    username = models.CharField(max_length=200, null=True)
    profilePic = models.ImageField(default='/default.jpg', upload_to=path_and_rename)
    bio = models.TextField(null=True, blank=True)
    followers_count = models.IntegerField(blank=True, null=True, default=0)
    followers = models.ManyToManyField(User, related_name='following', blank=True)
    email_verified = models.BooleanField(default=False)
    id = models.UUIDField(default=uuid4, unique=True, primary_key=True, editable=False)
    """
    profile = UserProfile.objects.first()
    profile.followers.all() -> All users following this profile
    user.following.all() -> All user profiles I follow
    """

    def __str__(self):
        return str(self.user.username)
