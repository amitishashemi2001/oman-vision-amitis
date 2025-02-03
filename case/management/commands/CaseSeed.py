import sys
from django.core.management.base import BaseCommand
import random
from case.models import CaseLog ,CaseSubStep , Case , CaseSubStepStatus
from accounts.models import User
from sys import stdout
from django.db import connection
from django.db.models import Q
from django.db.models.signals import post_save
from django.dispatch import receiver
from case.signals import create_case_log_signal

class Command(BaseCommand):
    def handle(self, *args, **options):
        flush_table(Case)
        create_case()

def flush_table(model):
    stdout.write('Flushing data from Case table...\n')
    table_name = model._meta.db_table
    with connection.cursor() as cursor:
        cursor.execute(f'TRUNCATE TABLE {table_name} RESTART IDENTITY CASCADE')

def create_case():
    stdout.write("Creating Cases....\n")
    post_save.disconnect(receiver=create_case_log_signal, sender=Case)

    expert = User.objects.filter(Q(is_staff=False) & Q(is_superuser=False) & Q(is_active=True)).first()
    admin = User.objects.filter(Q(is_staff=True) & Q(is_superuser=False) & Q(is_active=True)).first()

    case1 = Case.objects.create(
        expert=expert,
        admin=admin,
        head_first_name="John",
        head_last_name="Doe",
        job_title="Engineer",
        iran_phone_number="1234567890",
        oman_phone_number="0987654321",
        address="123 Main St",
        email="john.doe@example.com",
        bank_card_number="1234-5678-9012-3456",
        passport_description="John's passport",
        image_description="John's image",
        case_status="ONGOING"
    )

    case2 = Case.objects.create(
        expert=expert,
        admin=admin,
        head_first_name="Jane",
        head_last_name="Smith",
        job_title="Doctor",
        iran_phone_number="2345678901",
        oman_phone_number="1987654321",
        address="456 Elm St",
        email="jane.smith@example.com",
        bank_card_number="2345-6789-0123-4567",
        passport_description="Jane's passport",
        image_description="Jane's image",
        case_status="ONGOING"
    )
    post_save.connect(receiver=create_case_log_signal, sender=Case)
