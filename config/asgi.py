# """
# ASGI config for config project.
#
# It exposes the ASGI callable as a module-level variable named ``application``.
#
# For more information on this file, see
# https://docs.djangoproject.com/en/3.2/howto/deployment/asgi/
# """
#
# import os
# from channels.auth import AuthMiddlewareStack
# from channels.routing import ProtocolTypeRouter, URLRouter
# from django.core.asgi import get_asgi_application
# from .routing import ws_pattern
# from django_channels_jwt_auth_middleware.auth import JWTAuthMiddlewareStack
#
#
#
#
# os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
# django_asgi_app = get_asgi_application()
#
# application = ProtocolTypeRouter({
#     # Django's ASGI application to handle traditional HTTP requests
#     "http": get_asgi_application(),
#
#     # WebSocket chat handler
#     "websocket": JWTAuthMiddlewareStack(URLRouter(ws_pattern))
#     #  "websocket": AuthMiddlewareStack(
#     #         URLRouter(
#     #             ws_pattern
#     #         )
#     # ),
# })
#
#

"""
ASGI config for mysite project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.0/howto/deployment/asgi/
"""

# import os
# from channels.routing import ProtocolTypeRouter, URLRouter
# from django_channels_jwt_auth_middleware.auth import JWTAuthMiddlewareStack
# from config import routing
# import django
# from django.core.asgi import get_asgi_application
#
#
# os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
# django_asgi_app = get_asgi_application()
# application = ProtocolTypeRouter({
#     "http": get_asgi_application(),
#     "https": get_asgi_application(),
#      "websocket": JWTAuthMiddlewareStack(
#          URLRouter(routing.ws_pattern)
#      ),
# })

import os

from django.core.asgi import get_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

application = get_asgi_application()



