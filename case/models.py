from django.db import models
from accounts.models import User
from django.conf import settings
from config.helpers import move_file
import os
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator
def validate_admin_user(value):
    if isinstance(value, int):
        user = User.objects.get(pk=value)
    else:
        user = value
    if not user.is_staff:
        raise ValidationError('کاربر انتخاب شده باید ادمین باشد')
def validate_expert_user(value):
    if isinstance(value, int):
        user = User.objects.get(pk=value)
    else:
        user = value
    if user.is_staff or user.is_superuser or not user.is_active:
        raise ValidationError('کاربر انتخاب شده باید کارشناس باشد')
class CaseStatus(models.TextChoices):
    ONGOING = 'ONGOING', 'در حال انجام'
    FINISHED = 'FINISHED', 'اتمام یافته'
    CANCELED = 'CANCELED', 'لغو شده'

class CaseSubStepStatus(models.TextChoices):
    INPROGRESS = 'INPROGRESS', 'در حال انجام'
    DONE = 'DONE', 'انجام شده'
    FAILED = 'FAILED', 'ناموفق'
    CANCELED = 'CANCELED', 'لغو شده'

class CaseSubStepDoer(models.TextChoices):
    EXPERT = 'EXPERT', 'کارشناس'
    ADMIN = 'ADMIN', 'ادمین'
class CaseSubStepType(models.TextChoices):
    TEXT = 'TEXT', 'متن'
    FILE = 'FILE', 'فایل'
class CaseStep(models.Model):
    step_name = models.CharField(verbose_name='نام مرحله', max_length=255, null=True, blank=True)
    description = models.CharField(verbose_name='توضیحات', max_length=255, null=True, blank=True)
    order = models.IntegerField(verbose_name='ترتیب', unique=True, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'مرحله پرونده'
        verbose_name_plural = 'مراحل پرونده'

    def __str__(self):
        return f'{self.step_name}'
class CaseSubStep(models.Model):
    step = models.ForeignKey(CaseStep, on_delete=models.CASCADE,
                             verbose_name='مرحله', related_name='substeps', null=True, blank=True)
    substep_name = models.CharField(verbose_name='نام زیرمرحله', max_length=255, null=True, blank=True)
    substep_hour_time = models.IntegerField(verbose_name='زمان زیرمرحله',
                                            null=True, blank=True, validators=[MinValueValidator(0)])
    is_start = models.BooleanField(verbose_name='شروع', default=False)
    type = models.CharField(verbose_name='نوع', choices=CaseSubStepType.choices, max_length=255, null=True, blank=True)
    description = models.CharField(verbose_name='توضیحات', max_length=255, null=True, blank=True)
    next = models.ForeignKey('self', on_delete=models.SET_NULL,
                             verbose_name='زیر مرحله بعدی', unique=True, null=True, blank=True, related_name='previous')
    doer = models.CharField(verbose_name='انجام دهنده',
                            choices=CaseSubStepDoer.choices, max_length=255, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'زیرمرحله پرونده'
        verbose_name_plural = 'زیرمراحل پرونده'

    def __str__(self):
        return f'{self.substep_name}'


class Case(models.Model):
    expert = models.ForeignKey(User, on_delete=models.SET_NULL,
                               verbose_name='کارشناس', related_name='expert_cases', null=True, blank=True)
    admin = models.ForeignKey(User, on_delete=models.SET_NULL, verbose_name='ادمین',
                              related_name='admin_cases', null=True, blank=True, validators=[validate_admin_user])
    head_first_name = models.CharField(verbose_name='نام', max_length=255, default='default name')
    head_last_name = models.CharField(verbose_name='نام خانوادگی', max_length=255, default='default lastname')
    job_title = models.CharField(verbose_name='عنوان شغلی', max_length=255, null=True, blank=True)

    work_address = models.CharField(verbose_name='نشانی محل کار', max_length=255, null=True, blank=True)
    home_address = models.CharField(verbose_name='نشانی منزل', max_length=255, null=True, blank=True)
    national_id = models.CharField(verbose_name='کد ملی', max_length=10, unique=True, null=True, blank=True)
    birth_year = models.PositiveIntegerField(verbose_name='سال تولد', null=True, blank=True)

    iran_phone_number = models.CharField(verbose_name='شماره تلفن ایران', max_length=255, null=True, blank=True)
    oman_phone_number = models.CharField(verbose_name='شماره تلفن عمان', max_length=255, null=True, blank=True)
    address = models.CharField(verbose_name='آدرس', max_length=255, null=True, blank=True)
    email = models.EmailField(verbose_name='ایمیل', max_length=255, null=True, blank=True)
    bank_card_number = models.CharField(verbose_name='شماره کارت بانکی', max_length=255, null=True, blank=True)
    passport = models.FileField(verbose_name='پاسپورت', upload_to='temp', null=True, blank=True)
    passport_description = models.TextField(verbose_name='توضیحات پاسپورت', null=True, blank=True)
    image = models.ImageField(verbose_name='عکس', upload_to='temp', null=True, blank=True)
    image_description = models.TextField(verbose_name='توضیحات عکس', null=True, blank=True)
    case_status = models.CharField(verbose_name='وضعیت پرونده',
                                   max_length=20, choices=CaseStatus.choices, default=CaseStatus.ONGOING)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    REQUIRED_FIELDS = ['head_first_name', 'head_last_name']

    class Meta:
        verbose_name = 'پرونده'
        verbose_name_plural = 'پرونده ها'

    def __str__(self):
        return f'{self.head_first_name} {self.head_last_name}'

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if self.passport:
            move_file(self.passport, os.path.join(settings.MEDIA_ROOT,
                                                  f'client/{self.id}/passport/{os.path.basename(self.passport.path)}'))
        if self.image:
            move_file(self.image, os.path.join(settings.MEDIA_ROOT,
                                               f'client/{self.id}/image/{os.path.basename(self.image.path)}'))
        super().save(update_fields=['passport', 'image'])

class CasePerson(models.Model):
    case = models.ForeignKey(Case, on_delete=models.CASCADE,
                             verbose_name='پرونده', related_name='persons', null=True, blank=True)
    order = models.PositiveIntegerField(verbose_name='ترتیب', null=True, blank=True, unique=True)
    first_name = models.CharField(verbose_name='نام', max_length=255, null=True, blank=True)
    last_name = models.CharField(verbose_name='نام خانوادگی', max_length=255, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'فرد پشنهادی'
        verbose_name_plural = 'افراد پشنهادی'

    def __str__(self):
        return f'{self.first_name} {self.last_name}'

class HeadRelative(models.Model):
    case = models.ForeignKey(Case, on_delete=models.CASCADE,
                             verbose_name='پرونده', related_name='relatives', null=True, blank=True)
    first_name = models.CharField(verbose_name='نام', max_length=255, null=True, blank=True)
    last_name = models.CharField(verbose_name='نام خانوادگی', max_length=255, null=True, blank=True)
    relation = models.CharField(verbose_name='نسبت', max_length=255, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'خویشاوند'
        verbose_name_plural = 'خویشاوندان'

    def __str__(self):
        return f'{self.first_name} {self.last_name}'

class CasePartner(models.Model):
    case = models.ForeignKey(Case, on_delete=models.CASCADE,
                             verbose_name='پرونده', related_name='partners', null=True, blank=True)
    first_name = models.CharField(verbose_name='نام', max_length=255, null=True, blank=True)
    last_name = models.CharField(verbose_name='نام خانوادگی', max_length=255, null=True, blank=True)
    percent = models.FloatField(verbose_name='درصد سهم', null=True, blank=True, validators=[MinValueValidator(0)])
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'شریک'
        verbose_name_plural = 'شرکا'

    def __str__(self):
        return f'{self.first_name} {self.last_name}'

class CaseService(models.Model):
    case = models.ForeignKey(Case, on_delete=models.CASCADE, verbose_name='پرونده',
                             related_name='services', null=True, blank=True)
    service = models.CharField(verbose_name='خدمات', max_length=255, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'خدمات'
        verbose_name_plural = 'خدمات'

    def __str__(self):
        return f'{self.id}'

class CompanySubject(models.Model):
    case = models.ForeignKey(Case, on_delete=models.CASCADE,
                             verbose_name='پرونده', related_name='company_subjects', null=True, blank=True)
    subject = models.CharField(verbose_name='موضوع', max_length=255, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'موضوع شرکت'
        verbose_name_plural = 'موضوعات شرکت'

    def __str__(self):
        return f'{self.subject}'

class CaseLog(models.Model):
    case = models.ForeignKey(Case, on_delete=models.CASCADE,
                             verbose_name='پرونده', related_name='case_logs', null=True, blank=True)
    substep = models.ForeignKey(CaseSubStep, on_delete=models.SET_NULL,
                                verbose_name='زیرمرحله', related_name='substep_logs', null=True, blank=True)
    substep_status = models.CharField(verbose_name='وضعیت زیرمرحله', max_length=20,
                                      choices=CaseSubStepStatus.choices, default=CaseSubStepStatus.INPROGRESS)
    description = models.TextField(verbose_name='توضیحات', null=True, blank=True)
    file = models.FileField(verbose_name='فایل', upload_to='temp', null=True, blank=True)
    date = models.DateTimeField(verbose_name='تاریخ', null=True, blank=True, auto_now_add=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'لاگ'
        verbose_name_plural = 'لاگ ها'

    def __str__(self):
        return f'{self.id}'

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if self.file and self.case:
            move_file(self.file, os.path.join(settings.MEDIA_ROOT,
                                              f'client/{self.case.id}/logs/{self.id}/'
                                              f'{os.path.basename(self.file.path)}'))
        super().save(update_fields=['file'])
