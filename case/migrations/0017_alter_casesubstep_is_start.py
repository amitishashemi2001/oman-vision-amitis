# Generated by Django 5.1.1 on 2024-10-27 12:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('case', '0016_remove_casesubstep_is_active_casesubstep_is_start'),
    ]

    operations = [
        migrations.AlterField(
            model_name='casesubstep',
            name='is_start',
            field=models.BooleanField(default=False, verbose_name='is_start'),
        ),
    ]
