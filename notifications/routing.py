from django.urls import re_path , path
from .consumers import NotificationsConsumer

websocket_urlpatterns = [
    # re_path(r'ws/socket-server/', consumers.ChatConsumer.as_asgi())
    path('', NotificationsConsumer.as_asgi())
]