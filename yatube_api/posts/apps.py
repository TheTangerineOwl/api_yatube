"""Файл конфигурации приложения работы с блогом."""
from django.apps import AppConfig


class PostsConfig(AppConfig):
    """Настройка приложения работы с блогом."""

    default_auto_field = 'django.db.models.BigAutoField'
    name = 'posts'
