# Generated by Django 5.0.1 on 2024-05-01 15:15

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0019_publishedhousing_status'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='MessagesRequest',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=50, verbose_name='Тема сообщения')),
                ('text', models.TextField(max_length=500, verbose_name='Сообщение')),
                ('reason', models.BooleanField(blank=True, default=None, null=True, verbose_name='Настроение сообщения')),
                ('date_push', models.DateTimeField(auto_now_add=True, verbose_name='Дата отправки')),
                ('publish_housing', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.publishedhousing', verbose_name='Публикация')),
                ('recipient', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='recipient_messages', to=settings.AUTH_USER_MODEL, verbose_name='Кому')),
                ('sender', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='sent_messages', to=settings.AUTH_USER_MODEL, verbose_name='От кого')),
            ],
            options={
                'verbose_name': 'Сообщение',
                'verbose_name_plural': 'Сообщения',
                'ordering': ['-date_push'],
            },
        ),
    ]
