# Generated by Django 5.0.1 on 2024-05-05 13:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0024_housing_city'),
    ]

    operations = [
        migrations.RemoveConstraint(
            model_name='buyrequest',
            name='unique_cart_item',
        ),
        migrations.AlterField(
            model_name='buyrequest',
            name='contract',
            field=models.FileField(blank=True, null=True, upload_to='contracts/%Y/%m/%d/', verbose_name='Договор'),
        ),
    ]
