from django.contrib.admin import models
from django.contrib.auth.models import AbstractUser, Group, Permission, GroupManager
from django.core.validators import RegexValidator

from django.db import models
from users.managers import CustomUserManager


class CustomUser(AbstractUser):
    REQUIRED_FIELDS = ['email']
    is_success = models.BooleanField(
        "success status",
        default=False,
        help_text="Определяет, подтвержденный ли аккаунт у пользователя",
    )
    patronymic = models.CharField(
        "Отчество",
        default=None,
        null=True, blank=True
    )
    passport_series = models.CharField('Серия паспорта', max_length=4, validators=[
        RegexValidator(regex=r'^\d{4}$', message='Серия паспорта должна состоять из 4 цифр')
    ], null=False)
    passport_number = models.CharField('Номер паспорта', max_length=6, validators=[
        RegexValidator(regex=r'^\d{6}$', message='Серия паспорта должна состоять из 6 цифр')
    ], null=False)
    passport_from = models.CharField('Кем выдан паспорт', max_length=100, null=False)
    passport_registration_address = models.CharField('Зарегистрирован по адресу', max_length=200, null=False)
    groups = models.ManyToManyField(
        'CustomGroup',
        verbose_name="Роли",
        related_name='users_roles'
    )

    objects = CustomUserManager()

    def __str__(self):
        return self.username

    def get_full_name(self):
        return f'{self.last_name} {self.first_name} {self.patronymic}'

    def get_initial(self):
        if self.patronymic:
            return f'{self.last_name} {self.first_name[0]}. {self.patronymic[0]}.'
        else:
            return f'{self.last_name} {self.first_name[0]}.'


class Codes(models.Model):
    code = models.CharField(max_length=50)
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)


class CustomGroup(models.Model):
    name = models.CharField("Название", max_length=150, unique=True)
    permissions = models.ManyToManyField(
        Permission,
        verbose_name="Права",
        blank=True,
    )
    users_guide = models.FileField('Руководство пользователя', upload_to='guids/', null=True, blank=True)

    objects = GroupManager()

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Роль'
        verbose_name_plural = 'Роли'
