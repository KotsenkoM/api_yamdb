from django.contrib.auth import get_user_model
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from .validators import year_validator

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
    name = models.CharField(
        max_length=200, verbose_name='Название произведения'
    )
    year = models.IntegerField('Дата первой публикации',
                               validators=[year_validator])
    description = models.TextField(blank=True, null=True, default='')
    genre = models.ManyToManyField(Genre)
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        related_name='category_title',
        null=True,
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
        default=1, validators=[MinValueValidator(1), MaxValueValidator(10)]
    )

    class Meta:
        ordering = ['-pub_date']
        constraints = [
            models.UniqueConstraint(
                fields=['author', 'title'], name='author_title'
            )
        ]
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'

    def __str__(self):
        return self.text


class Comment(models.Model):
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='comments'
    )
    review = models.ForeignKey(
        Review, on_delete=models.CASCADE, related_name='comments'
    )
    text = models.TextField()
    pub_date = models.DateTimeField(auto_now_add=True, db_index=True)

    class Meta:
        ordering = ['-pub_date']
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'
