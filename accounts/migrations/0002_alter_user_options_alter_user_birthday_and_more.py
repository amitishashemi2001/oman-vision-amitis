# Generated by Django 5.1.1 on 2024-11-09 09:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='user',
            options={'verbose_name': 'کاربر', 'verbose_name_plural': 'کاربران'},
        ),
        migrations.AlterField(
            model_name='user',
            name='birthday',
            field=models.DateField(blank=True, max_length=255, null=True, verbose_name='تاریخ تولد'),
        ),
        migrations.AlterField(
            model_name='user',
            name='company_email',
            field=models.EmailField(blank=True, max_length=254, null=True, unique=True, verbose_name='ایمیل شرکت'),
        ),
        migrations.AlterField(
            model_name='user',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='email',
            field=models.EmailField(max_length=254, unique=True, verbose_name='ایمیل'),
        ),
        migrations.AlterField(
            model_name='user',
            name='first_name',
            field=models.CharField(max_length=255, verbose_name='نام'),
        ),
        migrations.AlterField(
            model_name='user',
            name='is_active',
            field=models.BooleanField(default=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='is_deleted',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='user',
            name='is_staff',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='user',
            name='last_name',
            field=models.CharField(max_length=255, verbose_name='نام خانوادگی'),
        ),
        migrations.AlterField(
            model_name='user',
            name='phone_number',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='شماره تلفن'),
        ),
        migrations.AlterField(
            model_name='user',
            name='profile_image',
            field=models.ImageField(blank=True, null=True, upload_to='temp', verbose_name='عکس پروفایل'),
        ),
        migrations.AlterField(
            model_name='user',
            name='sex',
            field=models.CharField(choices=[('MALE', 'MALE'), ('FEMALE', 'FEMALE'), ('OTHER', 'OTHER')], default='OTHER', verbose_name='جنسیت'),
        ),
        migrations.AlterField(
            model_name='user',
            name='updated_at',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='username',
            field=models.CharField(default='', max_length=255, unique=True, verbose_name='نام کاربری'),
        ),
    ]
