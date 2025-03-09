"""Представления для классов группы, поста и комментариев."""
from rest_framework import viewsets
from rest_framework.exceptions import PermissionDenied, NotAuthenticated

from posts.models import Group, Post, Comment
from .serializers import (CommentSerializer, PostSerializer,
                          GroupSerializer)


class PostViewSet(viewsets.ModelViewSet):
    """Представление поста."""

    queryset = Post.objects.all()
    serializer_class = PostSerializer

    def perform_create(self, serializer):
        """Создание нового поста при POST-запросе."""
        serializer.save(author=self.request.user)

    def perform_update(self, serializer):
        """Обновление данных поста при PUT- или PATCH-запросе."""
        if not self.request.user.is_authenticated:
            raise NotAuthenticated()
        if self.request.user != serializer.instance.author:
            raise PermissionDenied()
        super().perform_update(serializer)

    def perform_destroy(self, instance):
        """Удаление поста при DELETE-запросе."""
        if not self.request.user.is_authenticated:
            raise NotAuthenticated()
        if self.request.user != instance.author:
            raise PermissionDenied()
        super().perform_destroy(instance)


class GroupViewSet(viewsets.ReadOnlyModelViewSet):
    """Представление группы постов (только для чтения)."""

    queryset = Group.objects.all()
    serializer_class = GroupSerializer


class CommentViewSet(viewsets.ModelViewSet):
    """Представление комментария к посту."""

    serializer_class = CommentSerializer

    def get_queryset(self):
        """Получения списка комментариев к заданному посту (GET-запрос)."""
        post_id = self.kwargs.get('post_id')
        return Comment.objects.filter(post_id=post_id)

    def perform_create(self, serializer):
        """Создание комментария к заданному посту при POST-запросе."""
        if not self.request.user.is_authenticated:
            raise NotAuthenticated()
        post_id = self.kwargs.get('post_id')
        serializer.save(author=self.request.user, post_id=post_id)

    def perform_update(self, serializer):
        """Обновление заданного комментария при PUT- или PATCH-запросе."""
        if not self.request.user.is_authenticated:
            raise NotAuthenticated()
        if serializer.instance.author != self.request.user:
            raise PermissionDenied()
        serializer.save()

    def perform_destroy(self, instance):
        """Удаление заданного комментария при DELETE-запросе."""
        if not self.request.user.is_authenticated:
            raise NotAuthenticated()
        if instance.author != self.request.user:
            raise PermissionDenied()
        instance.delete()
