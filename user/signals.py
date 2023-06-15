from django.contrib.auth.models import User
from user.models import UserProfile
from chat.models import Thread

from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
from django.db.models.signals import m2m_changed
from django.dispatch import receiver


# @receiver(m2m_changed, sender=UserProfile.followers.through)
# def create_thread_on_follow(sender, instance, action, reverse, pk_set, **kwargs):
#     if action == 'post_add':
#         for pk in pk_set:
#             user = User.objects.get(pk=pk)
#             if not Thread.objects.filter(sender=instance, reciever=user).exists():
#                 thread = Thread.objects.create(sender=instance, reciever=user)
#                 thread.save()

def updateUser(sender, instance, **kwargs):
    user = instance
    # if user.email != '':
    #     user.username = user.email
    
def updateUserProfile(sender, instance, **kwargs):
    user_prof = instance
    user_prof.username = user_prof.user.username


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(
            user=instance, 
            name=instance.username, 
            username=instance.username
        )



pre_save.connect(updateUser, sender=User)
pre_save.connect(updateUserProfile, sender=UserProfile)
post_save.connect(create_user_profile, sender=User)
