"""Сериализаторы для API для пользователя, постов, их групп и комментариев."""
from rest_framework import serializers
from posts.models import User, Post, Group, Comment


class UserSerializer(serializers.ModelSerializer):
    """Сериализатор для класса пользователя."""

    posts = serializers.StringRelatedField(many=True, read_only=True)

    class Meta:
        """Метаданные."""

        model = User
        fields = ('id', 'username', 'first_name', 'last_name', 'posts')


class GroupSerializer(serializers.ModelSerializer):
    """Сериализатор для класса группы постов."""

    group_title = serializers.CharField(source='title')

    class Meta:
        """Метаданные."""

        model = Group
        # fields = ('group_title', 'slug', 'description')
        fields = '__all__'


class CommentSerializer(serializers.ModelSerializer):
    """Сериализатор для класса комментария к посту."""

    post = serializers.PrimaryKeyRelatedField(read_only=True)
    author = serializers.StringRelatedField(read_only=True)

    class Meta:
        """Метаданные."""

        model = Comment
        # fields = ('author', 'post', 'text', 'created')
        fields = '__all__'
        read_only_fields = ('post', 'author', )


class PostSerializer(serializers.ModelSerializer):
    """Сериализатор для класса постов в блоге."""

    author = serializers.StringRelatedField(read_only=True)
    group = serializers.StringRelatedField()

    class Meta:
        """Метаданные."""

        model = Post
        # fields = ('text', 'pub_date', 'author', 'image', 'group', 'comments')
        fields = '__all__'
        read_only_fields = ('author', )
