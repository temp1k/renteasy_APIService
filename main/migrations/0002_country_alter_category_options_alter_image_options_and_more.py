# Generated by Django 5.0.1 on 2024-02-27 09:04

import django.core.validators
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Country',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, unique=True, verbose_name='Страна')),
                ('code_name', models.CharField(blank=True, max_length=5, null=True, verbose_name='Кодовое название')),
            ],
        ),
        migrations.AlterModelOptions(
            name='category',
            options={'verbose_name': 'Категория', 'verbose_name_plural': 'Категории'},
        ),
        migrations.AlterModelOptions(
            name='image',
            options={'verbose_name': 'Изображение', 'verbose_name_plural': 'Изображения'},
        ),
        migrations.CreateModel(
            name='Housing',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(unique=True, verbose_name='Название жилья')),
                ('short_name', models.CharField(verbose_name='Сокращенное название')),
                ('date_creation', models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')),
                ('address', models.CharField(blank=True, null=True, verbose_name='Адрес')),
                ('number_of_seats', models.PositiveIntegerField(verbose_name='Количество мест')),
                ('description', models.TextField(null=True, verbose_name='Описание')),
                ('rating', models.DecimalField(decimal_places=1, default=0, max_digits=2, validators=[django.core.validators.MaxValueValidator(5), django.core.validators.MinValueValidator(0)])),
                ('country', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='main.country', verbose_name='Страна')),
            ],
            options={
                'verbose_name': 'Жилье',
                'verbose_name_plural': 'Жилье',
            },
        ),
    ]