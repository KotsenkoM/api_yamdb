from django.contrib.auth.models import AbstractUser
from django.db import models


class UserRoles:
    USER = "user"
    MODERATOR = "moderator"
    ADMIN = "admin"
    choices = (
        (USER, USER),
        (MODERATOR, MODERATOR),
        (ADMIN, ADMIN),
    )


class User(AbstractUser):
    username = models.CharField(
        max_length=50, unique=True,
        blank=True, verbose_name='Пользователь'
    )
    email = models.EmailField(
         blank=False, unique=True, verbose_name='Электронная почта'
    )
    bio = models.TextField(
        'Биография', blank=True,
    )
    role = models.CharField(
        max_length=10, choices=UserRoles.choices,
        default=UserRoles.USER, verbose_name="Роль",
    )
    confirmation_code = models.CharField(
        max_length=30, editable=False, blank=True,
        null=True, unique=True, verbose_name='Код подтверждения')
