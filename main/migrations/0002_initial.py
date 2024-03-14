# Generated by Django 5.0.1 on 2024-03-14 10:37

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('main', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='favorite',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.customuser', verbose_name='Пользователь'),
        ),
        migrations.AddField(
            model_name='feedback',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL, verbose_name='Пользователь'),
        ),
        migrations.AddField(
            model_name='housing',
            name='categories',
            field=models.ManyToManyField(related_name='housings', to='main.category', verbose_name='Категории'),
        ),
        migrations.AddField(
            model_name='housing',
            name='country',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='housings', to='main.country', verbose_name='Страна'),
        ),
        migrations.AddField(
            model_name='housing',
            name='owner',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL, verbose_name='Владелец'),
        ),
        migrations.AddField(
            model_name='housingimages',
            name='housing',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='images', to='main.housing', verbose_name='Жилье'),
        ),
        migrations.AddField(
            model_name='housingimages',
            name='image',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='main.image', verbose_name='Изображение'),
        ),
        migrations.AddField(
            model_name='publishedhousing',
            name='housing',
            field=models.OneToOneField(on_delete=django.db.models.deletion.PROTECT, to='main.housing', verbose_name='Жилье'),
        ),
        migrations.AddField(
            model_name='feedback',
            name='product',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='feedbacks', to='main.publishedhousing', verbose_name='Товар'),
        ),
        migrations.AddField(
            model_name='favorite',
            name='product',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.publishedhousing', verbose_name='Избранный товар'),
        ),
        migrations.AddField(
            model_name='customuser',
            name='favorites',
            field=models.ManyToManyField(related_name='Товар', through='main.Favorite', to='main.publishedhousing'),
        ),
        migrations.AddField(
            model_name='housing',
            name='tags',
            field=models.ManyToManyField(related_name='housings', to='main.tag', verbose_name='Теги'),
        ),
        migrations.AddField(
            model_name='housing',
            name='types',
            field=models.ManyToManyField(related_name='housings', to='main.typehousing', verbose_name='Типы жилья'),
        ),
    ]
