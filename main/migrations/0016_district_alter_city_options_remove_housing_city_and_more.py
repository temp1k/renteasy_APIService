# Generated by Django 5.0.1 on 2024-04-23 08:48

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0015_city_remove_housing_country_remove_housing_types_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='District',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, unique=True, verbose_name='Округ')),
                ('code_name', models.CharField(max_length=100, unique=True, verbose_name='Кодовое название')),
            ],
            options={
                'verbose_name': 'Округ',
                'verbose_name_plural': 'Округ',
            },
        ),
        migrations.AlterModelOptions(
            name='city',
            options={'verbose_name': 'Город', 'verbose_name_plural': 'Город'},
        ),
        migrations.RemoveField(
            model_name='housing',
            name='city',
        ),
        migrations.AddField(
            model_name='housing',
            name='district',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, related_name='housings', to='main.district', verbose_name='Округ'),
        ),
    ]
