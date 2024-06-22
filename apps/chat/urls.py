from django.urls import path
from .views import RoomListView, RoomView
from .models.ajax import (
    message_feedback_dissatisfaction_update_ajax,
    message_feedback_dissatisfaction_comment_ajax,
    room_settings_pagenate_ajax,
)

app_name = 'chat'

urlpatterns = [
    path('',                     RoomListView.as_view(),   name='room_list'),
    path('room/<str:room_id>',   RoomView.as_view(),       name='room'),
    # MessageFeedback Ajax
    path('ajax/chat/message_feedback_dissatisfaction_update_ajax',  message_feedback_dissatisfaction_update_ajax,  name='message_feedback_dissatisfaction_update_ajax'),
    path('ajax/chat/message_feedback_dissatisfaction_comment_ajax', message_feedback_dissatisfaction_comment_ajax, name='message_feedback_dissatisfaction_comment_ajax'),
    # RoomSettings Ajax
    path('ajax/chat/room_settings_pagenate_ajax', room_settings_pagenate_ajax, name='room_settings_pagenate_ajax'),
]