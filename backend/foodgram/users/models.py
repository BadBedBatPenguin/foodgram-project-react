from datetime import date

# from recipes.models import Recipe

from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

GUEST = 'guest'
USER = 'user'
ADMIN = 'admin'
ROLE_CHOICES = [
    (GUEST, 'гость'),
    (USER, 'пользователь'),
    (ADMIN, 'администратор'),
]


class User(AbstractUser):
    email = models.EmailField(
        'Электронная почта',
        unique=True,
        max_length=254,
    )
    first_name = models.CharField(
        'Имя',
        max_length=150
    )
    last_name = models.CharField(
        'Фамилия',
        max_length=150
    )
    password = models.CharField(
        'Пароль',
        max_length=150
    )

    # favourites = models.ManyToManyField(
    #     to=Recipe,
    #     verbose_name='Избранное',
    #     blank=True,
    # )

    REQUIRED_FIELDS = ['email', 'first_name', 'last_name']

    def is_admin(self):
        return (
            self.role == ADMIN
            or self.is_staff
        )

    def is_user(self):
        return self.role == USER

    def __str__(self):
        return self.username

    class Meta:
        ordering = ('username',)
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
