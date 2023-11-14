from django.urls import path
from .views import (
    RoomListView, RoomView,
    RoomCreateView, RoomDeleteView
)

app_name = 'chat'

urlpatterns = [
    path('',                     RoomListView.as_view(),   name='room_list'),
    path('room/<str:room_id>',   RoomView.as_view(),       name='room'),
    path('create/',              RoomCreateView.as_view(), name='room_create'),
    path('delete/<str:room_id>', RoomDeleteView.as_view(), name='room_delete'),
]