import datetime
import sys
import time
from django.utils import timezone
from django.core.management.base import BaseCommand
import random
from case.models import CaseLog, CaseSubStep, Case, CaseSubStepStatus
from sys import stdout
from django.db import connection

class Command(BaseCommand):
    def handle(self, *args, **options):
        flush_table(CaseLog)
        create_case_log()

def flush_table(model):
    stdout.write('Flushing data from CaseLog table...\n')
    table_name = model._meta.db_table
    with connection.cursor() as cursor:
        cursor.execute(f'TRUNCATE TABLE {table_name} RESTART IDENTITY CASCADE')

def create_case_log():
    stdout.write("Creating CaseLogs....\n")
    cases = Case.objects.all()
    substep = CaseSubStep.objects.get(is_start=True)
    for case in cases:
        CaseLog.objects.create(
                               case=case,
                               substep=substep,
                               description="description",
                               date=timezone.now()
                               )
