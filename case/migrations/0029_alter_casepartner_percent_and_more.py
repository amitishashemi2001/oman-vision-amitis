# Generated by Django 5.1.1 on 2024-12-03 11:24

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('case', '0028_casesubstep_substep_hour_time_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='casepartner',
            name='percent',
            field=models.FloatField(blank=True, null=True, validators=[django.core.validators.MinValueValidator(0)], verbose_name='درصد سهم'),
        ),
        migrations.AlterField(
            model_name='casesubstep',
            name='substep_hour_time',
            field=models.IntegerField(blank=True, null=True, validators=[django.core.validators.MinValueValidator(0)], verbose_name='زمان زیرمرحله'),
        ),
    ]
