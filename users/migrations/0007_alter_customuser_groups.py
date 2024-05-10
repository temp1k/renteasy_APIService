# Generated by Django 5.0.1 on 2024-05-07 13:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0006_customgroup'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='groups',
            field=models.ManyToManyField(blank=True, null=True, related_name='users_roles', to='users.customgroup', verbose_name='Группы'),
        ),
    ]