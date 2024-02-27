# -*- coding: utf-8 -*-
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models


class Image(models.Model):
    image = models.ImageField('Изображение', null=False, blank=False, upload_to='images')
    date_creation = models.DateTimeField('Дата создания', auto_now_add=True)
    date_update = models.DateTimeField('Дата обновления', auto_now=True)

    def __str__(self):
        return self.image

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


class Housing(models.Model):
    name = models.CharField('Название жилья', unique=True)
    short_name = models.CharField('Сокращенное название', null=True, blank=True)
    date_creation = models.DateTimeField('Дата создания', auto_now_add=True)
    date_update = models.DateTimeField('Дата обновления', auto_now=True)
    address = models.CharField('Адрес', blank=True, null=True)
    number_of_seats = models.PositiveIntegerField('Количество мест')
    description = models.TextField('Описание', null=True)
    country = models.ForeignKey(Country, on_delete=models.PROTECT, verbose_name='Страна')
    rating = models.DecimalField(max_digits=2, decimal_places=1, default=0, validators=[
            MaxValueValidator(5),
            MinValueValidator(0)
        ])

    def __str__(self):
        return f'{self.name} ({self.country})'

    class Meta:
        verbose_name = 'Жилье'
        verbose_name_plural = 'Жилье'
