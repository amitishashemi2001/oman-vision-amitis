# Generated by Django 5.1.1 on 2024-12-01 12:53

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Message',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100, verbose_name='عنوان')),
                ('description', models.TextField(blank=True, null=True, verbose_name='توضیحات')),
                ('status', models.CharField(choices=[('NEW', 'New'), ('INPROGRESS', 'Inprogress'), ('CLOSED', 'Closed')], default='NEW', max_length=20, verbose_name='حالت')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('admin', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='admin_tickets', to=settings.AUTH_USER_MODEL, verbose_name='ادمین')),
                ('expert', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='expert_tickets', to=settings.AUTH_USER_MODEL, verbose_name='کارشناس')),
            ],
            options={
                'verbose_name': 'گفتگو',
                'verbose_name_plural': 'گفتگو ها',
            },
        ),
        migrations.CreateModel(
            name='MessageRecord',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.TextField(verbose_name='محتوا')),
                ('is_deleted', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('Message', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='records', to='message.message', verbose_name='گفتگو')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='messages', to=settings.AUTH_USER_MODEL, verbose_name='شخص')),
            ],
            options={
                'verbose_name': 'پیام',
                'verbose_name_plural': 'پیام ها',
            },
        ),
    ]
