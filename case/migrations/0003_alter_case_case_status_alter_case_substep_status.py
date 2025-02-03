# Generated by Django 5.1.1 on 2024-10-22 10:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('case', '0002_rename_status_case_case_status_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='case',
            name='case_status',
            field=models.CharField(choices=[('ONGOING', 'ONGOING'), ('FINISHED', 'FINISHED'), ('FAILED', 'FAILED')], default='ONGOING', max_length=20, verbose_name='case_status'),
        ),
        migrations.AlterField(
            model_name='case',
            name='substep_status',
            field=models.CharField(choices=[('NEW', 'NEW'), ('DONE', 'DONE'), ('FAILED', 'FAILED')], default='NEW', max_length=20, verbose_name='substep_status'),
        ),
    ]
