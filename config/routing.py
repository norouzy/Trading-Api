from django.urls import path
from api import consumer

ws_pattern= [
    path('ws/user_info/',consumer.TradeConsumer.as_asgi()),
    path('ws/homeData/', consumer.HomePageConsumer.as_asgi()),
]

