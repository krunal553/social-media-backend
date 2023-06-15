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


class Post (models.Model):
    _id = models.AutoField(primary_key=True, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts', null=True, blank=True)
    profilePic = models.ImageField(null=True, blank=True, upload_to=path_and_rename, max_length=1000)
    desc = models.TextField(null=True, blank=True)
    image = models.ImageField(null=True, blank=True, upload_to=path_and_rename, max_length=1000)
    likes_count = models.IntegerField(blank=True, null=True, default=0)
    likers = models.ManyToManyField(User, related_name='likes', blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.desc 


class PostComment (models.Model):
    id = models.AutoField(primary_key=True, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    # name = models.ForeignKey(User, default=User.first_name, on_delete=models.CASCADE)
    post_id = models.ForeignKey(Post, related_name='comments', on_delete=models.CASCADE)
    comment_text = models.TextField(null=True, blank=True)
    commented_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.user.username + self.comment_text)