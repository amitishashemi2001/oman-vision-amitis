from rest_framework.serializers import (PrimaryKeyRelatedField, Serializer, ModelSerializer,
                                        SerializerMethodField, IntegerField)
from .models import Chat, ChatMessage
from accounts.models import User
from accounts.serializers import UserDetailChatListSerializer
class ChatSerializer(ModelSerializer):
    class Meta:
        model = Chat
        fields = '__all__'
class UserChatListSerializer(Serializer):
    id = IntegerField()
    user_data = SerializerMethodField()
    admin_info = SerializerMethodField()

    def get_user_data(self, obj):
        user = obj.assignee if obj.assigner == self.context['request'].user else obj.assigner
        return UserDetailChatListSerializer(user).data

    def get_admin_info(self, obj):
        admin_user = obj.assigner if obj.assigner.is_admin else obj.assignee
        return {
            "id": admin_user.id,
            "first_name": admin_user.first_name,
            "last_name": admin_user.last_name,
            "profile_image": admin_user.profile_image.url if admin_user.profile_image else None
        }

class ChatMessageSerializer(ModelSerializer):
    chat = PrimaryKeyRelatedField(write_only=True, queryset=Chat.objects.all())
    user = PrimaryKeyRelatedField(write_only=True, queryset=User.objects.all())
    is_writer = SerializerMethodField()

    class Meta:
        model = ChatMessage
        exclude = ['is_deleted']
        read_only_fields = ['is_seen']

    def get_is_writer(self, obj):
        return obj.is_written_by(self.context['request'].user)
class ChatMessageUpdateDestroySerializer(ModelSerializer):
    class Meta:
        model = ChatMessage
        fields = ['content']
