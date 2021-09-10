from django.contrib.auth.models import AbstractUser, UserManager
from django.db import models


class User(AbstractUser):
    bio = models.TextField(
        'biography',
        blank=True,
    )
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=150, unique=True)

    EMAIL_FIELD = 'email'
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    objects = UserManager()