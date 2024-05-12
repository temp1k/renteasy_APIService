# Generated by Django 5.0.1 on 2024-05-07 13:11

import django.contrib.auth.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        # ('auth', '0016_remove_group_users_guide'),
        ('users', '0005_alter_customuser_passport_number'),
    ]

    operations = [
        migrations.CreateModel(
            name='CustomGroup',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=150, unique=True, verbose_name='Название')),
                ('users_guide', models.FileField(blank=True, null=True, upload_to='guids/', verbose_name='Руководство пользователя')),
                ('permissions', models.ManyToManyField(blank=True, to='auth.permission', verbose_name='Права')),
            ],
            options={
                'verbose_name': 'Роль',
                'verbose_name_plural': 'Роли',
            },
            managers=[
                ('objects', django.contrib.auth.models.GroupManager()),
            ],
        ),
    ]
