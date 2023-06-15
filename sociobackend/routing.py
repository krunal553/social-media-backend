from django.urls import path
from channels.routing import  URLRouter

from notifications.routing import websocket_urlpatterns as notifications_ws_urlpatterns
from chat.routing import websocket_urlpatterns as chat_ws_urlpatterns

websocket_routes = [
    path("ws/notifications/", URLRouter(notifications_ws_urlpatterns)),
    path("ws/chat/", URLRouter(chat_ws_urlpatterns)),
    # path("ws/app2/", URLRouter(app2_ws_urlpatterns)),
]