# Generated by Django 5.1.1 on 2024-10-23 08:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('case', '0003_alter_case_case_status_alter_case_substep_status'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='case',
            name='substep_status',
        ),
        migrations.AddField(
            model_name='caselog',
            name='substep_status',
            field=models.CharField(choices=[('NEW', 'NEW'), ('DONE', 'DONE'), ('INPROGRESS', 'INPROGRESS'), ('FAILED', 'FAILED')], default='NEW', max_length=20, verbose_name='substep_status'),
        ),
    ]
