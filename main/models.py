# -*- coding: utf-8 -*-
from datetime import datetime

import pytz
from django.contrib.auth import get_user_model
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.db.models import Avg
from rest_framework.exceptions import ValidationError

User = get_user_model()


class Image(models.Model):
    image = models.ImageField('Изображение', null=False, blank=False, upload_to='images')
    date_creation = models.DateTimeField('Дата создания', auto_now_add=True)
    date_update = models.DateTimeField('Дата обновления', auto_now=True)

    def __str__(self):
        return self.image.url

    class Meta:
        verbose_name = 'Изображение'
        verbose_name_plural = 'Изображения'


class Category(models.Model):
    name = models.CharField('Название категории', max_length=255, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'


class District(models.Model):
    name = models.CharField('Округ', unique=True, max_length=100)
    code_name = models.CharField('Кодовое название', unique=True, max_length=100)

    def __str__(self):
        return f'{self.name} округ'

    class Meta:
        verbose_name = 'Округ'
        verbose_name_plural = 'Округа'


class City(models.Model):
    name = models.CharField('Город', unique=True, max_length=100)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Город'
        verbose_name_plural = 'Города'


class Currency(models.Model):
    name = models.CharField('Название', unique=True)
    code = models.CharField('Кодовое название', unique=True, max_length=4)
    publish_name = models.CharField('Сокращенное название', max_length=5)
    value = models.DecimalField('Значение', max_digits=12, decimal_places=5, null=True, blank=True)

    def __str__(self):
        return self.code

    class Meta:
        verbose_name = 'Валюта'
        verbose_name_plural = 'Валюты'


class Housing(models.Model):
    name = models.CharField('Название жилья', unique=True)
    short_name = models.CharField('Сокращенное название', null=True, blank=True)
    date_creation = models.DateTimeField('Дата создания', auto_now_add=True)
    date_update = models.DateTimeField('Дата обновления', auto_now=True)
    city = models.ForeignKey(City, on_delete=models.PROTECT, verbose_name='Город', related_name='housings')
    address = models.CharField('Адрес')
    number_of_seats = models.PositiveIntegerField('Количество мест', default=1)
    description = models.TextField('Описание', null=True)
    district = models.ForeignKey(District, on_delete=models.PROTECT, verbose_name='Округ', related_name='housings')
    rating = models.DecimalField(max_digits=2, decimal_places=1, default=0, validators=[
        MaxValueValidator(5),
        MinValueValidator(0)
    ])
    owner = models.ForeignKey(User, verbose_name='Владелец', on_delete=models.PROTECT)
    categories = models.ManyToManyField('Category', verbose_name='Категории', related_name='housings')
    tags = models.ManyToManyField('Tag', verbose_name='Теги', related_name='housings', null=True, blank=True)
    metro = models.ForeignKey('Metro', verbose_name='Метро', on_delete=models.PROTECT, null=True, blank=True)
    images = models.ManyToManyField('Image', verbose_name='Изображения', through='HousingImages',
                                    related_name='housing', null=False, blank=False)

    def __str__(self):
        return f'{self.name} ({self.district})'

    class Meta:
        verbose_name = 'Жилье'
        verbose_name_plural = 'Жилье'


class HousingImages(models.Model):
    housing = models.ForeignKey(Housing, verbose_name='Жилье', on_delete=models.CASCADE)
    image = models.OneToOneField(Image, verbose_name='Изображение', on_delete=models.CASCADE, unique=True)

    def __str__(self):
        return f'{self.housing.name} image: {self.image}'

    class Meta:
        verbose_name = 'Изображение жилья'
        verbose_name_plural = 'Изображения жилья'


class Tag(models.Model):
    name = models.CharField('Название тега', unique=True)

    def __str__(self):
        return f'{self.name}'

    class Meta:
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'


class Metro(models.Model):
    name = models.CharField('Метро', unique=True)
    city = models.ForeignKey(City, verbose_name='Город', on_delete=models.PROTECT)

    def __str__(self):
        return f'{self.name}'

    class Meta:
        verbose_name = 'Метро'
        verbose_name_plural = 'Метро'


class PublicationStatus(models.Model):
    name = models.CharField('Статус публикации', unique=True, max_length=50)

    def __str__(self):
        return f'{self.name}'

    class Meta:
        verbose_name = 'Статус публикации'
        verbose_name_plural = 'Статусы публикации'


class PublishedHousing(models.Model):
    housing = models.OneToOneField(Housing, verbose_name='Жилье', on_delete=models.PROTECT)
    date_publish = models.DateField('Дата публикации', auto_now_add=True)
    date_begin = models.DateTimeField('Дата начала')
    date_end = models.DateTimeField('Дата конца')
    activity = models.BooleanField('Активность', default=True, db_default=True)
    status = models.ForeignKey(PublicationStatus, verbose_name='Статус публикации', on_delete=models.PROTECT)
    price = models.DecimalField('Цена за одно место', max_digits=12, decimal_places=2)
    currency = models.ForeignKey(Currency, verbose_name='Валюта', on_delete=models.PROTECT)

    def __str__(self):
        return self.housing.__str__()

    def clean(self, *args, **kwargs):
        # run the base validation
        super(PublishedHousing, self).clean(*args, **kwargs)

        # Don't allow dates older than now.
        if self.date_begin < datetime.now(pytz.UTC):
            raise ValidationError('Begin date must be later than now.')
        if self.date_end < datetime.now(pytz.UTC) or self.date_end < self.date_begin:
            raise ValidationError('End date must be later than now and later than the begin date.')

    class Meta:
        verbose_name = 'Опубликованное жилье'
        verbose_name_plural = 'Опубликованное жилье'


class MessagesRequest(models.Model):
    publish_housing = models.ForeignKey(PublishedHousing, verbose_name='Публикация', on_delete=models.CASCADE)
    sender = models.ForeignKey(User, verbose_name='От кого', related_name='sent_messages', on_delete=models.CASCADE)
    recipient = models.ForeignKey(User, verbose_name='Кому', related_name='recipient_messages', on_delete=models.CASCADE)
    title = models.CharField('Тема сообщения', max_length=50)
    text = models.TextField('Сообщение', max_length=500)
    reason = models.BooleanField('Настроение сообщения', null=True, blank=True, default=None)
    date_push = models.DateTimeField('Дата отправки', auto_now_add=True)

    def __str__(self):
        return f'Уведомление от {self.sender.username} к {self.recipient.username} по поводу {self.publish_housing}'

    class Meta:
        verbose_name = 'Уведомление'
        verbose_name_plural = 'Уведомления'
        ordering = ['-date_push']


class Feedback(models.Model):
    estimation = models.IntegerField('Оценка', validators=[
        MaxValueValidator(5),
        MinValueValidator(0)
    ])
    description = models.TextField('Отзыв', null=True, blank=True)
    date_push = models.DateTimeField('Дата публикации', auto_now_add=True)
    product = models.ForeignKey(PublishedHousing, verbose_name='Товар',
                                related_name='feedbacks', on_delete=models.CASCADE)
    user = models.ForeignKey(User, verbose_name='Пользователь', on_delete=models.PROTECT)

    def __str__(self):
        return f'Отзыв {self.user.username} от {self.date_push}'

    def clean(self):
        # Проверяем уникальность сочетания product и user
        if Feedback.objects.filter(product=self.product, user=self.user).exists():
            raise ValidationError('Данный пользователь уже писал отзыв к данному продукту')

    def save(self, *args, **kwargs):
        super(Feedback, self).save(*args, **kwargs)

        # После сохранения отзыва, пересчитываем средний рейтинг жилья
        average_rating = Feedback.objects.filter(product=self.product).aggregate(Avg('estimation'))['estimation__avg']

        print(average_rating)

        if average_rating is not None:
            self.product.housing.rating = round(average_rating, 1)
            self.product.housing.save()

    class Meta:
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'
        unique_together = ('product', 'user')
        ordering = ['-date_push']


class Favorite(models.Model):
    product = models.ForeignKey(PublishedHousing, on_delete=models.CASCADE, verbose_name='Избранный товар')
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Пользователь', related_name='Favorites')
    date_creation = models.DateTimeField('Дата добавления', auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['product', 'user'], name='unique_favorite')
        ]


class Chat(models.Model):
    housing = models.ForeignKey(PublishedHousing, on_delete=models.CASCADE, verbose_name='Жилье')
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Пользователь', related_name='users')

    def __str__(self):
        return f'{self.user.username} c {self.housing.name}'

    class Meta:
        verbose_name = 'Чат'
        verbose_name_plural = 'Чаты'


class Message(models.Model):
    text = models.TextField('Текст сообщения')
    date_push = models.DateTimeField('Дата отправки', auto_now_add=True)
    chat = models.ForeignKey(Chat, on_delete=models.CASCADE, verbose_name='Чат', related_name='messages')
    user = models.ForeignKey(User, on_delete=models.CASCADE,
                             related_name='messages', verbose_name='Пользователь')

    def __str__(self):
        return f'Сообщение {self.user.username} в чате {self.chat.id} || {self.date_push}'

    class Meta:
        verbose_name = 'Сообщение'
        verbose_name_plural = 'Сообщения'


class BuyRequest(models.Model):
    product = models.ForeignKey(PublishedHousing, on_delete=models.CASCADE, verbose_name='Товар')
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Пользователь', related_name='cart')
    number_of_seats = models.PositiveIntegerField('Количество мест')
    date_begin = models.DateTimeField('Дата начала')
    date_end = models.DateTimeField('Дата конца')
    price = models.DecimalField('Цена', max_digits=12, decimal_places=2)
    owner_confirm = models.BooleanField('Подтверждение хозяина', default=False)
    buyer_confirm = models.BooleanField('Подтверждение покупателя', default=True)
    contract = models.FileField('Договор',  upload_to='contracts/%Y/%m/%d/', null=True, blank=True,)

    class Meta:
        constraints = [
        ]

    def clean(self):
        super().clean()
        if self.product.housing.number_of_seats < self.number_of_seats:
            raise ValidationError(
                {'number_of_seats': f'Превышен лимит доступного места.'
                                    f' Максимум {self.product.housing.number_of_seats} '
                                    f'мест, а указано {self.number_of_seats}'})

        if self.product.date_begin > self.date_begin or self.product.date_end < self.date_end:
            raise ValidationError(
                {'date_error': 'Неверно указаны даты'}
            )
