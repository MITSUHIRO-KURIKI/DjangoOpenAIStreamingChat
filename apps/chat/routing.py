from django.urls import path
from .consumers import OpenAIChatConsumer

websocket_urlpatterns = [
    path('ws/chat/room/<str:room_id>', OpenAIChatConsumer.as_asgi()),
]