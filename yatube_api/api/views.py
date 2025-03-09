from rest_framework import viewsets
from rest_framework.exceptions import PermissionDenied, NotAuthenticated

from posts.models import Group, Post, Comment

from .serializers import (CommentSerializer, PostSerializer,
                          GroupSerializer)


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def perform_update(self, serializer):
        if not self.request.user.is_authenticated:
            raise NotAuthenticated()
        if self.request.user != serializer.instance.author:
            raise PermissionDenied()
        super().perform_update(serializer)

    def perform_destroy(self, instance):
        if not self.request.user.is_authenticated:
            raise NotAuthenticated()
        if self.request.user != instance.author:
            raise PermissionDenied()
        super().perform_destroy(instance)

    # @action(detail=True, methods=['GET', 'PUT', 'PATCH', 'DELETE'])
    # def post_detail(self, request, pk):
    #     post = get_object_or_404(Post, pk=pk)

    #     if request.method == 'GET':
    #         serializer = self.get_serializer(post)
    #         return Response(serializer.data, status=status.HTTP_200_OK)

    #     user = request.user
    #     if not user.is_authenticated:
    #         return Response(status=status.HTTP_401_UNAUTHORIZED)

    #     # Проверка на авторство поста
    #     if user != post.author:
    #         return Response(status=status.HTTP_403_FORBIDDEN)

    #     if request.method in ['PUT', 'PATCH']:
    #         serializer = PostSerializer(post, data=request.data, partial=True)
    #         if serializer.is_valid():
    #             serializer.save()
    #             return Response(serializer.data,
    #                             status=status.HTTP_200_OK)
    #         return Response(serializer.errors,
    #                         status=status.HTTP_400_BAD_REQUEST)

    #     elif request.method == 'DELETE':
    #         post.delete()
    #         return Response(status=status.HTTP_204_NO_CONTENT)

    # @action(detail=False, methods=['GET', 'POST'])
    # def post_list(self, request):
    #     posts = Post.objects.all()
    #     if request.method == 'GET':
    #         serializer = PostSerializer(posts, many=True)
    #         return Response(serializer.data, status=status.HTTP_200_OK)
    #     # user = request.user
    #     if not request.user.is_authenticated:
    #         return Response(status=status.HTTP_401_UNAUTHORIZED)
    #     if request.method == 'POST':
    #         serializer = PostSerializer(data=request.data)
    #         if serializer.is_valid():
    #             serializer.save()
    #             return Response(serializer.data,
    #                             status=status.HTTP_201_CREATED)
    #         return Response(serializer.errors,
    #                         status=status.HTTP_400_BAD_REQUEST)


class GroupViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer

    def get_queryset(self):
        post_id = self.kwargs.get('post_id')
        return Comment.objects.filter(post_id=post_id)

    def perform_create(self, serializer):
        if not self.request.user.is_authenticated:
            raise NotAuthenticated()
        post_id = self.kwargs.get('post_id')
        serializer.save(author=self.request.user, post_id=post_id)

    def perform_update(self, serializer):
        if not self.request.user.is_authenticated:
            raise NotAuthenticated()
        if serializer.instance.author != self.request.user:
            raise PermissionDenied()
        serializer.save()

    def perform_destroy(self, instance):
        if not self.request.user.is_authenticated:
            raise NotAuthenticated()
        if instance.author != self.request.user:
            raise PermissionDenied()
        instance.delete()
