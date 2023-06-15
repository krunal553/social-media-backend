import os
from daphne import server

from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from django.conf.urls.static import static
from django.conf import settings
from django.urls import re_path
from django.views.static import serve

from .routing import websocket_routes


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sociobackend.settings')

# application = get_asgi_application()
# def static(prefix, view=serve, **kwargs):
#     # Use the correct prefix argument
#     return [
#         re_path(r'^%s(?P<path>.*)$' % prefix.lstrip('/'), view, kwargs=kwargs),
#     ]


application = ProtocolTypeRouter({
    'http':get_asgi_application(),
    'websocket':AuthMiddlewareStack(
        URLRouter(
            websocket_routes
        ),
    ),
    #  "static": static(settings.STATIC_URL, document_root=settings.STATIC_ROOT),
    # "media": static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT),


})

# application = static(application, document_root=settings.MEDIA_ROOT)
