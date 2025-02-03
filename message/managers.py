from django.db.models.manager import Manager
class MessageRecordManager(Manager):
    def get_queryset(self):
        return super().get_queryset().filter(is_deleted=False)
