from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser
from django.db import models
from phonenumber_field.modelfields import PhoneNumberField

from userApp.constants import NULLABLE
from userApp.services import generate_invite_code


class UserManager(BaseUserManager):
    def create_user(self, phone_number, password=None, **extra_fields):
        if not phone_number:
            raise ValueError('The Phone Number field must be set')
        user = self.model(phone_number=phone_number, **extra_fields)
        user.set_password(password)
        user.invite_code = generate_invite_code()  # Здесь присваивается инвайт-код
        user.save(using=self._db)
        return user

    def create_superuser(self, phone_number, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(phone_number, password, **extra_fields)


class User(AbstractUser):
    username = None
    avatar = models.ImageField(
        upload_to='users',
        verbose_name='Аватар',
        help_text='Загрузите свое фото'
    )
    phone_number = PhoneNumberField(
        unique=True,
        region='RU',
        verbose_name='Номер телефона',
        help_text='Укажите ваш номер телефона'
    )
    invite_code = models.CharField(
        max_length=6,
        unique=True,
        **NULLABLE,
        verbose_name='Инвайт код'
    )
    activated_invite_code = models.CharField(
        max_length=6,
        **NULLABLE,
        verbose_name='Активированный инвайт код'
    )
    verification_code = models.CharField(
        max_length=4,
        **NULLABLE,
        verbose_name='Код верификации'
    )
    country = models.CharField(
        max_length=100,
        **NULLABLE,
        verbose_name='Страна',
        help_text='Укажите свою страну'
    )
    city = models.CharField(
        max_length=100,
        **NULLABLE,
        verbose_name='Город',
        help_text='Укажите город в котором вы живете'
    )

    objects = UserManager()

    USERNAME_FIELD = 'phone_number'
    REQUIRED_FIELDS = []

    def __str__(self):
        return f"{self.phone_number}, {self.first_name}"

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
