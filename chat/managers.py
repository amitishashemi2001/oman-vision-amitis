from django.db.models.manager import Manager
class ChatMessageManager(Manager):
    def get_queryset(self):
        return super().get_queryset().filter(is_deleted=False)
