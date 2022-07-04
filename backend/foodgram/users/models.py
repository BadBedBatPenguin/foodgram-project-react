from datetime import date

# from recipes.models import Recipe

from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.shortcuts import get_object_or_404

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
    role = models.CharField(
        max_length=max(len(role) for _, role in ROLE_CHOICES),
        choices=ROLE_CHOICES,
        default=USER,
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


class Follow(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        related_name='follower',
        verbose_name='Подписчик',
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        related_name='following',
        verbose_name='Автор',
    )

    def __str__(self) -> str:
        return f'{self.user} подписан на {self.author}'

    class Meta:
        verbose_name = 'Подписка'
        verbose_name_plural = 'Подписки'
