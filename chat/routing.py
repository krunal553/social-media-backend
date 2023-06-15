from django.urls import re_path , path
from .consumers import ChatConsumer

websocket_urlpatterns = [
    # re_path(r'ws/socket-server/', consumers.ChatConsumer.as_asgi())
    # re_path(r'(?P<thread_id>\d+)/$', ChatConsumer.as_asgi())
    re_path(r'(?P<thread_id>[0-9a-f]{8}-[0-9a-f]{4}-[4][0-9a-f]{3}-[8-9a-b][0-9a-f]{3}-[0-9a-f]{12})/$', ChatConsumer.as_asgi())

    # path('', ChatConsumer.as_asgi())
]