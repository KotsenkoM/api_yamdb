from django.contrib.auth.models import AbstractUser, UserManager
from django.core import validators
from django.db import models


class UserRoles:
    USER = 'user'
    MODERATOR = 'moderator'
    ADMIN = 'admin'
    choices = (
        (USER, USER),
        (MODERATOR, MODERATOR),
        (ADMIN, ADMIN),
    )


class User(AbstractUser):
    bio = models.TextField(
        verbose_name='О себе', blank=True, null=True, max_length=200
    )
    role = models.CharField(
        verbose_name='Роль пользователя',
        max_length=10,
        default=UserRoles.USER,
        choices=UserRoles.choices,
    )
    email = models.EmailField(
        verbose_name='Электронная почта',
        validators=[validators.validate_email],
        unique=True,
    )
    confirmation_code = models.CharField(null=True, blank=True, max_length=255)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['confirmation_code', 'username']

    def __str__(self):
        return self.email

    @property
    def is_admin(self):
        return self.role == UserRoles.ADMIN or self.is_superuser

    @property
    def is_moderator(self):
        return self.role == UserRoles.MODERATOR

    @property
    def is_user(self):
        return self.role == UserRoles.USER

    objects = UserManager()
