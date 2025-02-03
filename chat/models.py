from django.db import models
from accounts.models import User
from .managers import ChatMessageManager
# Create your models here.
class Chat(models.Model):
    assigner = models.ForeignKey(User, related_name='assigner_chats', on_delete=models.CASCADE)
    assignee = models.ForeignKey(User, related_name='assignee_chats', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.assigner} {self.assignee}"

    def get_admin_info(self):
        return {
            "id": self.assigner.id,
            "first_name": self.assigner.first_name,
            "last_name": self.assigner.last_name,
            "profile_image": self.assigner.profile_image.url if self.assigner.profile_image else None
        }


class ChatMessage(models.Model):
    chat = models.ForeignKey(Chat, related_name='records', on_delete=models.CASCADE)
    user = models.ForeignKey(User, related_name='chat_messages', on_delete=models.CASCADE)
    content = models.TextField()
    is_seen = models.BooleanField(default=False)
    is_deleted = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = ChatMessageManager()

    def is_written_by(self, user):
        return self.user == user

    def __str__(self):
        return f"id {self.id} user{self.user}"
