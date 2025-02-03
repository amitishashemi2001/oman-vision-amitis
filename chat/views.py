from rest_framework.generics import (CreateAPIView,
                                     DestroyAPIView, ListAPIView, UpdateAPIView)
from rest_framework.permissions import IsAuthenticated
from .models import Chat, ChatMessage
from .serializers import (ChatSerializer, UserChatListSerializer,
                          ChatMessageSerializer, ChatMessageUpdateDestroySerializer)
import sys
from rest_framework.response import Response
from django.db.models import Q
from .pagination import ChatMessagePagination

# Create your views here.

class ChatCreateAPIView(CreateAPIView):
    queryset = Chat.objects.all()
    serializer_class = ChatSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        try:
            user = request.user.id
            assignee = request.data.get('assignee')

            if user == assignee:
                return Response('You cannot assign a chat to yourself', status=400)

            if Chat.objects.filter(
                Q(assigner=user, assignee=assignee) |
                Q(assigner=assignee, assignee=user)
            ).exists():
                return Response('A chat with this assigner and assignee already exists', status=400)

            request.data['assigner'] = request.user.id
            return self.create(request, *args, **kwargs)
        except Exception as e:
            print(f'Error in ChatCreateAPIView: {e}', file=sys.stderr)
            return Response(f'Error in ChatCreate: {e}', status=400)
class UserChatListAPIView(ListAPIView):
    serializer_class = UserChatListSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        chats = Chat.objects.filter(Q(assigner=user) | Q(assignee=user))
        return chats.select_related('assigner', 'assignee')

class ChatDestroyAPIView(DestroyAPIView):
    queryset = Chat.objects.all()
    serializer_class = ChatSerializer
    permission_classes = [IsAuthenticated]
class ChatMessageCreateAPIView(CreateAPIView):
    queryset = ChatMessage.objects.all()
    serializer_class = ChatMessageSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        try:
            request.data['user'] = request.user.id
            return self.create(request, *args, **kwargs)
        except Exception as e:
            print(f'Error in ChatMessageCreateAPIView: {e}', file=sys.stderr)
            return Response(f'Error in ChatMessageCreate: {e}', status=400)
class ChatMessageListAPIView(ListAPIView):
    serializer_class = ChatMessageSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = ChatMessagePagination

    def get_queryset(self):
        chat_id = self.kwargs['pk']
        chat = Chat.objects.get(id=chat_id)
        messages = chat.records.order_by('created_at')
        return messages

    def get(self, request, *args, **kwargs):
        try:
            chat = Chat.objects.get(id=self.kwargs['pk'])
            messages = chat.records.filter(is_seen=False).exclude(user=request.user)
            for message in messages:
                message.is_seen = True
                message.save()
            return super().get(request, *args, **kwargs)
        except Exception as e:
            print(f'Error in ChatMessageListAPIView: {e}', file=sys.stderr)
            return Response(f'Error in ChatMessageList: {e}', status=400)
class ChatMessageUpdateDestroyAPIView(UpdateAPIView, DestroyAPIView):
    queryset = ChatMessage.objects.filter(is_deleted=False)
    serializer_class = ChatMessageUpdateDestroySerializer
    permission_classes = [IsAuthenticated]

    def delete(self, request, *args, **kwargs):
        try:
            message = self.get_object()
            message.is_deleted = True
            message.save()
            return Response('Message deleted', status=204)
        except Exception as e:
            print(f'Error in ChatMessageUpdateDestroyAPIView: {e}', file=sys.stderr)
            return Response(f'Error in ChatMessageUpdate or Destroy: {e}', status=400)
