# Generated by Django 5.0.1 on 2024-03-14 11:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0005_alter_chat_options_alter_feedback_options_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='publishedhousing',
            name='price',
            field=models.DecimalField(decimal_places=2, max_digits=12, verbose_name='Цена за одно место'),
        ),
    ]
