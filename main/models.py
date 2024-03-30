# -*- coding: utf-8 -*-
from datetime import datetime

import pytz
from django.contrib.auth import get_user_model
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
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


class Country(models.Model):
    name = models.CharField('Страна', unique=True, max_length=100)
    code_name = models.CharField('Кодовое название', max_length=5, null=True, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Страна'
        verbose_name_plural = 'Страны'


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
    address = models.CharField('Адрес')
    number_of_seats = models.PositiveIntegerField('Количество мест', default=1)
    description = models.TextField('Описание', null=True)
    country = models.ForeignKey(Country, on_delete=models.PROTECT, verbose_name='Страна', related_name='housings')
    rating = models.DecimalField(max_digits=2, decimal_places=1, default=0, validators=[
        MaxValueValidator(5),
        MinValueValidator(0)
    ])
    owner = models.ForeignKey(User, verbose_name='Владелец', on_delete=models.PROTECT)
    categories = models.ManyToManyField('Category', verbose_name='Категории', related_name='housings')
    tags = models.ManyToManyField('Tag', verbose_name='Теги', related_name='housings', null=True, blank=True)
    types = models.ManyToManyField('TypeHousing', verbose_name='Типы жилья', related_name='housings')
    images = models.ManyToManyField('Image', verbose_name='Изображения', through='HousingImages',
                                    related_name='housing', null=False, blank=False)

    def __str__(self):
        return f'{self.name} ({self.country})'

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


class TypeHousing(models.Model):
    name = models.CharField('Тип жилья', unique=True)

    def __str__(self):
        return f'{self.name}'

    class Meta:
        verbose_name = 'Тип жилья'
        verbose_name_plural = 'Типы жилья'


class PublishedHousing(models.Model):
    housing = models.OneToOneField(Housing, verbose_name='Жилье', on_delete=models.PROTECT)
    date_publish = models.DateField('Дата публикации', auto_now_add=True)
    date_begin = models.DateTimeField('Дата начала')
    date_end = models.DateTimeField('Дата конца')
    activity = models.BooleanField('Активность', default=True, db_default=True)
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


class Feedback(models.Model):
    estimation = models.IntegerField('Оценка', validators=[
        MaxValueValidator(5),
        MinValueValidator(0)
    ])
    description = models.TextField('Отзыв', null=True)
    date_push = models.DateTimeField('Дата публикации', auto_now_add=True)
    product = models.ForeignKey(PublishedHousing, verbose_name='Товар',
                                related_name='feedbacks', on_delete=models.CASCADE)
    user = models.ForeignKey(User, verbose_name='Пользователь', on_delete=models.PROTECT)

    def __str__(self):
        return f'Отзыв {self.user.username} от {self.date_push}'

    class Meta:
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'


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


class CartItem(models.Model):
    product = models.ForeignKey(PublishedHousing, on_delete=models.CASCADE, verbose_name='Товар в корзине')
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Владелец корзины', related_name='cart')
    number_of_seats = models.PositiveIntegerField('Количество мест')
    date_begin = models.DateTimeField('Дата начала')
    date_end = models.DateTimeField('Дата конца')

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['product', 'user'], name='unique_cart_item')
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
