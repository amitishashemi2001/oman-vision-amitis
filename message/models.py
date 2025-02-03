from django.db import models
from .managers import MessageRecordManager
from accounts.models import User
from case.models import validate_expert_user, validate_admin_user

# Create your models here.
class MessageStatus(models.TextChoices):
    NEW = 'NEW', 'جدید'
    INPROGRESS = 'INPROGRESS', 'باز'
    CLOSED = 'CLOSED', 'بسته شده'

class Message(models.Model):
    expert = models.ForeignKey(User, verbose_name='کارشناس', on_delete=models.CASCADE, related_name='expert_tickets',
                               null=True, blank=True, validators=[validate_expert_user])
    admin = models.ForeignKey(User, verbose_name='ادمین', on_delete=models.CASCADE, related_name='admin_tickets',
                              null=True, blank=True, validators=[validate_admin_user])
    title = models.CharField(verbose_name='عنوان', max_length=100)
    description = models.TextField(verbose_name='توضیحات', null=True, blank=True)
    status = models.CharField(verbose_name='حالت', max_length=20,
                              choices=MessageStatus.choices, default=MessageStatus.NEW)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'گفتگو'
        verbose_name_plural = 'گفتگو ها'

    def __str__(self):
        return self.title

class MessageRecord(models.Model):
    message = models.ForeignKey(Message, verbose_name='گفتگو', on_delete=models.CASCADE, related_name='records')
    user = models.ForeignKey(User, verbose_name='شخص', on_delete=models.CASCADE, related_name='messages')
    content = models.TextField(verbose_name='محتوا')
    is_deleted = models.BooleanField(verbose_name='پاک شده', default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = MessageRecordManager()

    class Meta:
        verbose_name = 'پیام'
        verbose_name_plural = 'پیام ها'

    def __str__(self):
        return self.content

    def is_written_by(self, user):
        return self.user == user
