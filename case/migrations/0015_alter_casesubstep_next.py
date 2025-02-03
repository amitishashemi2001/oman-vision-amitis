# Generated by Django 5.1.1 on 2024-10-27 10:13

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('case', '0014_remove_casesubstep_previous'),
    ]

    operations = [
        migrations.AlterField(
            model_name='casesubstep',
            name='next',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='previous', to='case.casesubstep', unique=True),
        ),
    ]
