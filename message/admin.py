from django.contrib import admin
from .models import Message , MessageRecord

# Register your models here.
admin.site.register(Message)
admin.site.register(MessageRecord)