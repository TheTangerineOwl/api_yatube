"""Модели блога (пользователь, группа постов, пост, комментарии к нему)."""
from django.contrib.auth import get_user_model
from django.db import models

# Модель пользователя.
User = get_user_model()


class Group(models.Model):
    """Группа постов."""

    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    description = models.TextField()

    def __str__(self):
        """Группа постов представляется своим названием."""
        return self.title


class Post(models.Model):
    """Пост в блоге."""

    text = models.TextField()
    pub_date = models.DateTimeField(
        'Дата публикации', auto_now_add=True
    )
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='posts'
    )
    image = models.ImageField(
        upload_to='posts/', null=True, blank=True
    )  # поле для картинки
    group = models.ForeignKey(
        Group, on_delete=models.SET_NULL,
        related_name='posts', blank=True, null=True
    )

    def __str__(self):
        """Пост представляется своим текстом."""
        return self.text


class Comment(models.Model):
    """Комментарий к посту."""

    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='comments'
    )
    post = models.ForeignKey(
        Post, on_delete=models.CASCADE, related_name='comments'
    )
    text = models.TextField()
    created = models.DateTimeField(
        'Дата добавления', auto_now_add=True, db_index=True
    )

    def __str__(self):
        """Комментарий представляется своим текстом."""
        return self.text
