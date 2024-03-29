# Generated by Django 5.0.1 on 2024-03-19 19:48

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0010_publishedhousing_currency'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.RemoveField(
            model_name='customuser',
            name='chats',
        ),
        migrations.RemoveField(
            model_name='customuser',
            name='favorites',
        ),
        migrations.RemoveField(
            model_name='customuser',
            name='user',
        ),
        migrations.AlterField(
            model_name='message',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='messages', to=settings.AUTH_USER_MODEL, verbose_name='Пользователь'),
        ),
        migrations.AlterField(
            model_name='favorite',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='Favorites', to=settings.AUTH_USER_MODEL, verbose_name='Пользователь'),
        ),
        migrations.AlterField(
            model_name='chat',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='users', to=settings.AUTH_USER_MODEL, verbose_name='Пользователь'),
        ),
        migrations.AlterField(
            model_name='publishedhousing',
            name='activity',
            field=models.BooleanField(db_default=models.Value(True), default=True, verbose_name='Активность'),
        ),
        migrations.AlterField(
            model_name='publishedhousing',
            name='currency',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='main.currency', verbose_name='Валюта'),
        ),
        migrations.AddConstraint(
            model_name='favorite',
            constraint=models.UniqueConstraint(fields=('product', 'user'), name='unique_favorite'),
        ),
        migrations.DeleteModel(
            name='CustomUser',
        ),
    ]
