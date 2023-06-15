from django.db import models
from user.models import UserProfile
from uuid import uuid4
from django.core.exceptions import ValidationError

class Thread(models.Model):
    thread_id = models.UUIDField(default=uuid4, unique=True, primary_key=True, editable=False)
    users = models.ManyToManyField(UserProfile)
    is_one_to_one = models.BooleanField(default=True)
    updated = models.DateTimeField(auto_now=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return ", ".join([user.username for user in self.users.all()])

    # def clean(self):
    #     super().clean()
    #     if self.is_one_to_one and self.users.count() != 2:
    #         raise ValidationError("One-to-one chat can only have 2 users.")

    # def save(self, *args, **kwargs):
    #     self.full_clean()
    #     super().save(*args, **kwargs)

class UserMessage(models.Model):
    id = models.UUIDField(default=uuid4,  unique=True, primary_key=True, editable=False)
    thread = models.ForeignKey(Thread, on_delete=models.CASCADE,related_name="messages")
    sender = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    body = models.TextField(null=True,blank=True)
    is_seen = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.body)