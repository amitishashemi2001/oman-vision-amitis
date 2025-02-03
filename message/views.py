from .serializers import MessageSerializer, MessageRecordSerializer, MessageRecordRetrieveUpdateDestroySerializer
from .models import Message, MessageRecord
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from accounts.permissions import IsExpertUser
from rest_framework.generics import ListCreateAPIView, ListAPIView, CreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.views import APIView
import sys
from rest_framework import status
from django.http import Http404, HttpResponseForbidden
from .paginations import MessageRecordPagination
from .permissions import check_user_is_record_owner
from rest_framework.response import Response
from .models import Device
from .utils import send_push_notification_to_admin

# Create your views here.

class AdminMessageListCreateAPIView(ListCreateAPIView):
    permission_classes = [IsAuthenticated, IsAdminUser]
    serializer_class = MessageSerializer

    def get_queryset(self):
        return Message.objects.filter(admin=self.request.user)

    def post(self, request, *args, **kwargs):
        try:
            request.data['admin'] = request.user.id
            return self.create(request, *args, **kwargs)
        except Exception as e:
            print(f'Error in AdminMessageListCreate post: {e}', file=sys.stderr)
            return Response(f'Error in AdminMessageListCreate post: {e}', status=400)
class ExpertMessageListCreateAPIView(ListCreateAPIView):
    permission_classes = [IsAuthenticated, IsExpertUser]
    serializer_class = MessageSerializer

    def get_queryset(self):
        return Message.objects.filter(expert=self.request.user)

    def post(self, request, *args, **kwargs):
        try:
            request.data['expert'] = request.user.id
            return self.create(request, *args, **kwargs)
        except Exception as e:
            print(f'Error in ExpertMessageListCreate post: {e}', file=sys.stderr)
            return Response(f'Error in ExpertMessageListCreate post: {e}', status=400)
class MessageRecordsListAPIView(ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = MessageRecordSerializer
    pagination_class = MessageRecordPagination

    def get_queryset(self):
        try:
            message = Message.objects.get(id=self.kwargs['pk'])
            return MessageRecord.objects.filter(message=message)
        except Message.DoesNotExist as e:
            raise Http404(f'{e}')
        except Exception as e:
            print(f'Error in MessageRecords List : {e}', file=sys.stderr)
class MessageRecordCreateAPIView(CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = MessageRecordSerializer
    queryset = MessageRecord.objects.all()

    def post(self, request, *args, **kwargs):
        try:
            message = Message.objects.get(id=request.data['message'])
            if message.status == 'NEW':
                message.status = 'INPROGRESS'
                message.save()
            request.data['user'] = request.user.id
            message_record = MessageRecord.objects.create(**request.data)

            if message.admin:
                admin_device = message.admin.device
                if admin_device:
                    player_id = admin_device.player_id
                    message_content = f"New message from expert: {message.title}"
                    send_push_notification_to_admin(player_id, message_content)

            return Response({"message": "Message record created and notification sent!"})
        except Exception as e:
            print(f'Error in MessageRecord Create: {e}', file=sys.stderr)
            return Response(f'Error in MessageRecord Create: {e}', status=400)

class MessageRecordRetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = MessageRecordRetrieveUpdateDestroySerializer
    queryset = MessageRecord.objects.all()

    def patch(self, request, *args, **kwargs):
        try:
            if not_allowed := check_user_is_record_owner(request.user, self.get_object()):
                return not_allowed
            return super().patch(request, *args, **kwargs)
        except Exception as e:
            print(f'Error in MessageRecord update: {e}', file=sys.stderr)
            return Response(f'Error in MessageRecord update: {e}', status=400)

    def put(self, request, *args, **kwargs):
        try:
            if not_allowed := check_user_is_record_owner(request.user, self.get_object()):
                return not_allowed
            return super().put(request, *args, **kwargs)
        except Exception as e:
            print(f'Error in MessageRecord update: {e}', file=sys.stderr)
            return Response(f'Error in MessageRecord update: {e}', status=400)

    def delete(self, request, *args, **kwargs):
        try:
            if not_allowed := check_user_is_record_owner(request.user, self.get_object()):
                return not_allowed
            record = self.get_object()
            record.is_deleted = True
            record.save()
            return Response('Message deleted', status=204)
        except Exception as e:
            print(f'Error in MessageRecord delete: {e}', file=sys.stderr)
            return Response(f'Error in MessageRecord delete: {e}', status=400)
class CloseMessageAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        try:
            message = Message.objects.get(id=self.kwargs['pk'])
            if request.user != (message.admin or message.expert):
                return HttpResponseForbidden('You are not allowed to close this message')
            if message.status == 'CLOSED':
                return Response('Message already closed', status=400)
            else:
                message.status = 'CLOSED'
                message.save()
                return Response('Message closed', status=200)
        except Exception as e:
            print(f'Error in CloseMessage: {e}', file=sys.stderr)
            return Response(f'Error in CloseMessage: {e}', status=400)


class SaveDeviceAPIView(APIView):
    def post(self, request, *args, **kwargs):
        player_id = request.data.get('player_id')
        device_type = request.data.get('device_type')  # Android, iOS, Web

        if player_id:
            device, created = Device.objects.get_or_create(user=request.user)
            device.player_id = player_id
            device.device_type = device_type
            device.save()

            return Response({"message": "Device saved successfully!"}, status=status.HTTP_201_CREATED)
        return Response({"error": "Player ID is required!"}, status=status.HTTP_400_BAD_REQUEST)
