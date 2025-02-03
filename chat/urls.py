from django.urls import path
from .views import (ChatCreateAPIView, UserChatListAPIView,
                    ChatDestroyAPIView, ChatMessageUpdateDestroyAPIView,
                    ChatMessageCreateAPIView, ChatMessageListAPIView)

urlpatterns = [
    path('chat/create/', ChatCreateAPIView.as_view(), name='chat-create'),
    path('user-chat/', UserChatListAPIView.as_view(), name='user-chat-list'),
    path('chat/<int:pk>/delete/', ChatDestroyAPIView.as_view(), name='chat-delete'),
    path('chat/message/create/', ChatMessageCreateAPIView.as_view(), name='message-create'),
    path('chat/message/<int:pk>/', ChatMessageUpdateDestroyAPIView.as_view(), name='message-update-delete'),
    path('chat/<int:pk>/messages/', ChatMessageListAPIView.as_view(), name='chat-messages'),
]
