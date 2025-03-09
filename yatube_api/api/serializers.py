from rest_framework import serializers
# from rest_framework.validators import UniqueTogetherValidator

# import datetime as dt

from posts.models import User, Post, Group, Comment


class UserSerializer(serializers.ModelSerializer):
    posts = serializers.StringRelatedField(many=True, read_only=True)

    class Meta:
        model = User
        fields = ('id', 'username', 'first_name', 'last_name', 'posts')
        ref_name = 'ReadOnlyUsers'


class GroupSerializer(serializers.ModelSerializer):
    group_title = serializers.CharField(source='title')

    class Meta:
        model = Group
        # fields = ('group_title', 'slug', 'description')
        fields = '__all__'


class CommentSerializer(serializers.ModelSerializer):
    post = serializers.PrimaryKeyRelatedField(read_only=True)
    # author = serializers.PrimaryKeyRelatedField(
    #     read_only=True, default=serializers.CurrentUserDefault()
    # )
    author = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Comment
        # fields = ('author', 'post', 'text', 'created')
        fields = '__all__'


class PostSerializer(serializers.ModelSerializer):
    # group = serializers.ManyRelatedField()
    # achievements = AchievementSerializer(many=True, required=False)
    # owner = serializers.PrimaryKeyRelatedField(read_only=True)
    # author = serializers.PrimaryKeyRelatedField(
    #     read_only=True, default=serializers.CurrentUserDefault())
    # group = serializers.PrimaryKeyRelatedField(required=False)
    # comments = CommentSerializer(many=True, required=False)
    author = serializers.StringRelatedField(read_only=True)
    group = serializers.StringRelatedField()

    class Meta:
        model = Post
        # fields = ('text', 'pub_date', 'author', 'image', 'group', 'comments')
        fields = '__all__'
        read_only_fields = ('author',)
