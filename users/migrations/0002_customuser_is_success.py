# Generated by Django 5.0.1 on 2024-04-23 09:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='is_success',
            field=models.BooleanField(default=False, help_text='Определяет, подтвержденный ли аккаунт у пользователя', verbose_name='success status'),
        ),
    ]
