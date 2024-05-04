# Generated by Django 5.0.1 on 2024-05-03 09:22

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0020_messagesrequest'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='messagesrequest',
            options={'ordering': ['-date_push'], 'verbose_name': 'Уведомление', 'verbose_name_plural': 'Уведомления'},
        ),
        migrations.CreateModel(
            name='BuyRequest',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('number_of_seats', models.PositiveIntegerField(verbose_name='Количество мест')),
                ('date_begin', models.DateTimeField(verbose_name='Дата начала')),
                ('date_end', models.DateTimeField(verbose_name='Дата конца')),
                ('price', models.DecimalField(decimal_places=2, max_digits=12, verbose_name='Цена')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.publishedhousing', verbose_name='Товар в корзине')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='cart', to=settings.AUTH_USER_MODEL, verbose_name='Владелец корзины')),
            ],
        ),
        migrations.DeleteModel(
            name='CartItem',
        ),
        migrations.AddConstraint(
            model_name='buyrequest',
            constraint=models.UniqueConstraint(fields=('product', 'user'), name='unique_cart_item'),
        ),
    ]
