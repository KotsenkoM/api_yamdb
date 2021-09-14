from django.contrib.auth import get_user_model
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

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


class Review(models.Model):
    text = models.TextField()
    pub_date = models.DateTimeField(
        'Дата добавления', auto_now_add=True, db_index=True
    )
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='reviews'
    )
    title = models.ForeignKey(
        Title, on_delete=models.CASCADE, related_name='reviews', null=True
    )
    score = models.IntegerField(
        default=1,
        validators=[MinValueValidator, MaxValueValidator])

    def __str__(self):
        return self.text
