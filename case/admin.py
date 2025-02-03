from django.contrib import admin
from django import forms
from .models import (Case, CasePerson, HeadRelative, CasePartner,
                     CaseService, CompanySubject, CaseStep, CaseLog, CaseSubStep)
import os
from django.conf import settings
import shutil
import sys
import time
from django.db import transaction


# Register your models here.

class CaseAdmin(admin.ModelAdmin):

    def delete_queryset(self, request, queryset):
        try:
            for obj in queryset:
                if obj.passport:
                    old_file_path = os.path.join(settings.MEDIA_ROOT, obj.passport.path)
                    if os.path.isfile(old_file_path):
                        new_file_path = os.path.join(settings.MEDIA_ROOT, 'backup',
                                                     f'client/{str(obj.id)}/passport/{time.time()}'
                                                     f'_{os.path.basename(old_file_path)}')
                        os.makedirs(os.path.dirname(new_file_path), exist_ok=True)
                        shutil.move(old_file_path, new_file_path)

                if obj.image:
                    old_file_path = os.path.join(settings.MEDIA_ROOT, obj.image.path)
                    if os.path.isfile(old_file_path):
                        new_file_path = os.path.join(settings.MEDIA_ROOT, 'backup',
                                                     f'client/{str(obj.id)}/image/{time.time()}'
                                                     f'_{os.path.basename(old_file_path)}')
                        os.makedirs(os.path.dirname(new_file_path), exist_ok=True)
                        shutil.move(old_file_path, new_file_path)
                if obj.case_logs:
                    for log in obj.case_logs.all():
                        if log.file:
                            old_file_path = os.path.join(settings.MEDIA_ROOT, log.file.path)
                            if os.path.isfile(old_file_path):
                                new_file_path = os.path.join(settings.MEDIA_ROOT, 'backup',
                                                             f'client/{str(obj.id)}/logs/{log.id}/{time.time()}'
                                                             f'_{os.path.basename(old_file_path)}')
                                os.makedirs(os.path.dirname(new_file_path), exist_ok=True)
                                shutil.move(old_file_path, new_file_path)

                folder_path = os.path.join(settings.MEDIA_ROOT, f'client/{str(obj.id)}')
                if os.path.isdir(folder_path):
                    shutil.rmtree(folder_path)
            super().delete_queryset(request, queryset)
        except Exception as e:
            print(f'error in admin delete queryset : {e}', file=sys.stderr)

    def delete_model(self, request, obj):
        try:
            if obj.passport:
                old_file_path = os.path.join(settings.MEDIA_ROOT, obj.passport.path)
                if os.path.isfile(old_file_path):
                    new_file_path = os.path.join(settings.MEDIA_ROOT, 'backup',
                                                 f'client/{str(obj.id)}/passport/{time.time()}'
                                                 f'_{os.path.basename(old_file_path)}')
                    os.makedirs(os.path.dirname(new_file_path), exist_ok=True)
                    shutil.move(old_file_path, new_file_path)

            if obj.image:
                old_file_path = os.path.join(settings.MEDIA_ROOT, obj.image.path)
                if os.path.isfile(old_file_path):
                    new_file_path = os.path.join(settings.MEDIA_ROOT, 'backup',
                                                 f'client/{str(obj.id)}/image/{time.time()}'
                                                 f'_{os.path.basename(old_file_path)}')
                    os.makedirs(os.path.dirname(new_file_path), exist_ok=True)
                    shutil.move(old_file_path, new_file_path)
            if obj.case_logs:
                for log in obj.case_logs.all():
                    if log.file:
                        old_file_path = os.path.join(settings.MEDIA_ROOT, log.file.path)
                        if os.path.isfile(old_file_path):
                            new_file_path = os.path.join(settings.MEDIA_ROOT, 'backup',
                                                         f'client/{str(obj.id)}/logs/{log.id}/{time.time()}'
                                                         f'_{os.path.basename(old_file_path)}')
                            os.makedirs(os.path.dirname(new_file_path), exist_ok=True)
                            shutil.move(old_file_path, new_file_path)

            folder_path = os.path.join(settings.MEDIA_ROOT, f'client/{str(obj.id)}')
            if os.path.isdir(folder_path):
                shutil.rmtree(folder_path)

            super().delete_model(request, obj)
        except Exception as e:
            print(f'error in admin delete model : {e}', file=sys.stderr)

    def save_model(self, request, obj, form, change):
        try:
            if change:
                instance = Case.objects.get(pk=obj.pk)
                if 'image' in form.changed_data and instance.image:
                    old_file_path = os.path.join(settings.MEDIA_ROOT, instance.image.path)
                    if os.path.isfile(old_file_path):
                        new_file_path = os.path.join(settings.MEDIA_ROOT, 'backup',
                                                     f'client/{str(obj.id)}/image/{time.time()}'
                                                     f'_{os.path.basename(old_file_path)}')
                        os.makedirs(os.path.dirname(new_file_path), exist_ok=True)
                        shutil.move(old_file_path, new_file_path)
                if 'passport' in form.changed_data and instance.passport:
                    old_file_path = os.path.join(settings.MEDIA_ROOT, instance.passport.path)
                    if os.path.isfile(old_file_path):
                        new_file_path = os.path.join(settings.MEDIA_ROOT, 'backup',
                                                     f'client/{str(obj.id)}/passport/{time.time()}'
                                                     f'_{os.path.basename(old_file_path)}')
                        os.makedirs(os.path.dirname(new_file_path), exist_ok=True)
                        shutil.move(old_file_path, new_file_path)
            super().save_model(request, obj, form, change)
        except Exception as e:
            print(f'error in admin save model : {e}', file=sys.stderr)

class CaseSubStepForm(forms.ModelForm):
    class Meta:
        model = CaseSubStep
        fields = '__all__'
        widgets = {
            'is_start': forms.CheckboxInput(),
        }

    def clean(self):

        return self.cleaned_data
class CaseSubStepAdmin(admin.ModelAdmin):
    form = CaseSubStepForm

    def save_model(self, request, obj, form, change):
        try:
            with transaction.atomic():
                if change:
                    if form.cleaned_data.get('is_start'):
                        for substep in CaseSubStep.objects.all():
                            substep.is_start = False
                            substep.save()
                    instance = CaseSubStep.objects.get(pk=obj.pk)
                    if form.cleaned_data.get('next'):
                        if exists := CaseSubStep.objects.filter(next_id=form.cleaned_data.get('next')).first():
                            exists_next = exists.next
                            exists.next = None
                            exists.save()
                            instance.next = exists_next
                        else:
                            instance.next = form.cleaned_data.get('next')
                    instance.step = form.cleaned_data.get('step')
                    instance.substep_name = form.cleaned_data.get('substep_name')
                    instance.is_start = form.cleaned_data.get('is_start')
                    instance.description = form.cleaned_data.get('description')
                    instance.doer = form.cleaned_data.get('doer')
                    instance.save()
                else:
                    if form.cleaned_data.get('is_start'):
                        for substep in CaseSubStep.objects.all():
                            substep.is_start = False
                            substep.save()
                    if form.cleaned_data.get('next'):
                        if exists := CaseSubStep.objects.filter(next_id=form.cleaned_data.get('next')).first():
                            exists_next = exists.next
                            exists.next = None
                            exists.save()
                            obj.next = exists_next
                        else:
                            obj.next = form.cleaned_data.get('next')
                    obj.step = form.cleaned_data.get('step')
                    obj.substep_name = form.cleaned_data.get('substep_name')
                    obj.is_start = form.cleaned_data.get('is_start')
                    obj.description = form.cleaned_data.get('description')
                    obj.doer = form.cleaned_data.get('doer')
                    obj.save()
        except Exception as e:
            print(f'error in save CaseSubStep AdminModel: {e}', file=sys.stderr)

class CaseLogAdmin(admin.ModelAdmin):
    # readonly_fields = ['case' , 'substep' , 'substep_status' ,
    # 'description' , 'file','date','created_at','updated_at']
    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False


admin.site.register(Case, CaseAdmin)
admin.site.register(HeadRelative)
admin.site.register(CasePartner)
admin.site.register(CaseService)
admin.site.register(CompanySubject)
admin.site.register(CasePerson)
admin.site.register(CaseStep)
admin.site.register(CaseLog, CaseLogAdmin)
admin.site.register(CaseSubStep, CaseSubStepAdmin)
