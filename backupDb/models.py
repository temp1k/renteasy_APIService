import logging

from django.core.management import call_command
from django.db import models
from django.dispatch import receiver
from django.db.models.signals import post_save

logger = logging.getLogger('django')


class Backup(models.Model):
    name = models.CharField('backup файл', max_length=255)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Backup'
        verbose_name_plural = 'Backups'
