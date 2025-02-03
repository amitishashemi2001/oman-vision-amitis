from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Case, CaseLog, CaseSubStep, CaseSubStepStatus

@receiver(post_save, sender=Case)
def create_case_log_signal(instance, created, **kwargs):
    if created:
        CaseLog.objects.create(
            case=instance,
            substep=CaseSubStep.objects.first(),
            substep_status=CaseSubStepStatus.INPROGRESS,
            description='Case Created',
            date=instance.created_at
        )
