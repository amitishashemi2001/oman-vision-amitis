from django.core.management.base import BaseCommand
from case.models import User
from sys import stdout
from django.db import connection

class Command(BaseCommand):
    def handle(self, *args, **options):
        flush_table(User)
        create_user()

def flush_table(model):
    stdout.write('Flushing data from User table...\n')
    table_name = model._meta.db_table
    with connection.cursor() as cursor:
        cursor.execute(f'TRUNCATE TABLE {table_name} RESTART IDENTITY CASCADE')

def create_user():
    stdout.write("Creating Users....\n")
    admin = User.objects.create_superuser(
        email="admin@admin.com",
        password="111",
        first_name="Admin",
        last_name="Admin",
    )
    admin2 = User.objects.create_superuser(
        email="admin2@admin2.com",
        password="111",
        first_name="Admin2",
        last_name="Admin2",
    )
    staff = User.objects.create_staff(
        email="staff@staff.com",
        password="111",
        first_name="Staff",
        last_name="Staff",
    )
    staff2 = User.objects.create_staff(
        email="staff2@staff2.com",
        password="111",
        first_name="Staff2",
        last_name="Staff2",
    )
    user = User.objects.create_user(
        email="user@user.com",
        password="111",
        first_name="User",
        last_name="User",
    )
    user2 = User.objects.create_user(
        email="user2@user2.com",
        password="111",
        first_name="User2",
        last_name="User2",
    )
