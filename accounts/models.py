from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, Group
from .managers import UserManager
from config.helpers import move_file
from django.conf import settings
import os
class Sex(models.TextChoices):
    MALE = 'MALE', 'مرد'
    FEMALE = 'FEMALE', 'زن'
    OTHER = 'OTHER', 'دیگر'
class User(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(verbose_name='نام کاربری', default='', unique=True, max_length=255)
    first_name = models.CharField(verbose_name='نام', max_length=255)
    last_name = models.CharField(verbose_name='نام خانوادگی', max_length=255)
    phone_number = models.CharField(verbose_name='شماره تلفن', max_length=255, null=True, blank=True)
    birthday = models.DateField(verbose_name='تاریخ تولد', max_length=255, null=True, blank=True)
    email = models.EmailField(verbose_name='ایمیل', unique=True)
    company_email = models.EmailField(verbose_name='ایمیل شرکت', unique=True, null=True, blank=True)
    sex = models.CharField(verbose_name='جنسیت', choices=Sex.choices, default=Sex.OTHER)
    profile_image = models.ImageField(verbose_name='عکس پروفایل', upload_to='temp', null=True, blank=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_deleted = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = ['first_name', 'last_name']
    objects = UserManager()

    class Meta:
        verbose_name = 'کاربر'
        verbose_name_plural = 'کاربران'

    def save(self, *args, **kwargs):
        if not self.username:
            self.username = self.email
        super().save(*args, **kwargs)
        if self.profile_image:
            move_file(self.profile_image, os.path.join(settings.MEDIA_ROOT, f'users/{self.id}/profile_image/'f'{os.
                                                       path.basename(self.profile_image.path)}'))
            super().save(update_fields=['profile_image'])

    def delete(self, using=None, keep_parents=False):
        self.is_deleted = True
        self.save()

    def __str__(self):
        return f'{self.first_name} {self.last_name}'
