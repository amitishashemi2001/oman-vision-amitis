from django.core.management.base import BaseCommand
import random
from case.models import CaseStep
from sys import stdout
from django.db import connection

class Command(BaseCommand):
    def handle(self, *args, **options):
        flush_table(CaseStep)
        create_case_step()

def flush_table(model):
    stdout.write('Flushing data from CaseStep table...\n')
    table_name = model._meta.db_table
    with connection.cursor() as cursor:
        cursor.execute(f'TRUNCATE TABLE {table_name} RESTART IDENTITY CASCADE')

def create_case_step():
    stdout.write("Creating CaseSteps....\n")

    steps = [
        {
            "step_name": "احراز هویت مشتری",
            "description": "description",
            "order": 1,
        },
        {
            "step_name": "ثبت شرکت",
            "description": "description",
            "order": 2,
        },
        {
            "step_name": "ارسال CR",
            "description": "description",
            "order": 3,
        },
        {
            "step_name": "دریافت لایسنس",
            "description": "description",
            "order": 4,
        },
        {
            "step_name": "دریافت مجوز کار",
            "description": "description",
            "order": 5,
        },
        {
            "step_name": "دریافت ویزا",
            "description": "description",
            "order": 6,
        },
        {
            "step_name": "ورود به عمان",
            "description": "description",
            "order": 7,
        },
        {
            "step_name": "انجام مراحل پزشکی در عمان",
            "description": "description",
            "order": 8,
        },
        {
            "step_name": "دریافت ID_CARD",
            "description": "description",
            "order": 9,
        },
        {
            "step_name": "باز کردن حساب بانکی",
            "description": "description",
            "order": 10,
        },
    ]
    for step in steps:
        CaseStep.objects.create(**step)

