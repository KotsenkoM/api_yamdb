from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class Genre(models.Model):
    name = models.CharField(max_length=50, verbose_name='Жанр')
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.name


class Category(models.Model):
    name = models.CharField(max_length=50, verbose_name='Категория')
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.name


class Title(models.Model):
    name = models.CharField(max_length=200,
                            verbose_name='Название произведения')
    year = models.IntegerField(
        'Дата первой публикации')
    description = models.TextField(blank=True, null=True, default='')
    genre = models.ManyToManyField(Genre)
    category = models.ForeignKey(
        Category, on_delete=models.SET_NULL,
        related_name="category_title", null=True
    )

    def __str__(self):
        return self.name
