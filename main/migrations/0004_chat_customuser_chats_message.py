# Generated by Django 5.0.1 on 2024-03-14 11:06

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0003_alter_housing_tags'),
    ]

    operations = [
        migrations.CreateModel(
            name='Chat',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('housing', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.publishedhousing', verbose_name='Жилье')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.customuser', verbose_name='Пользователь')),
            ],
        ),
        migrations.AddField(
            model_name='customuser',
            name='chats',
            field=models.ManyToManyField(related_name='Жилье', through='main.Chat', to='main.publishedhousing'),
        ),
        migrations.CreateModel(
            name='Message',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.TextField(verbose_name='Текст сообщения')),
                ('date_push', models.DateTimeField(auto_now_add=True, verbose_name='Дата отправки')),
                ('chat', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='messages', to='main.chat', verbose_name='Чат')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='messages', to='main.customuser', verbose_name='Пользователь')),
            ],
        ),
    ]
