from channels.routing import ProtocolTypeRouter,URLRouter
from channels.auth import AuthMiddlewareStack
from django.urls import path
from api import consumer
# from .middleware import TokenAuthMiddleware
from django_channels_jwt_auth_middleware.auth import JWTAuthMiddlewareStack

ws_pattern= [
    path('ws/user_info/',consumer.TradeConsumer.as_asgi()),
]

application= ProtocolTypeRouter(
    {
        'websocket':JWTAuthMiddlewareStack(URLRouter(ws_pattern))
    }
)