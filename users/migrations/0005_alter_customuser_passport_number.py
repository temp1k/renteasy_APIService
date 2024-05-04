# Generated by Django 5.0.1 on 2024-05-04 16:42

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0004_customuser_passport_from_customuser_passport_number_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='passport_number',
            field=models.CharField(max_length=6, validators=[django.core.validators.RegexValidator(message='Серия паспорта должна состоять из 6 цифр', regex='^\\d{6}$')], verbose_name='Номер паспорта'),
        ),
    ]
