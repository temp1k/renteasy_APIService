# -*- coding: utf-8 -*-
from django.db import models


class Image(models.Model):
    image = models.ImageField('Изображение', null=False, blank=False, upload_to='images')

    def __str__(self):
        return self.image

    class Meta:
        verbose_name = 'Изображение'
        verbose_name_plural = 'Изображения'


class Category(models.Model):
    name = models.CharField('Название категории', max_length=255)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
