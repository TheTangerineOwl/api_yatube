"""Пути для запросов к API."""
from django.urls import include, path
from rest_framework.authtoken import views
from rest_framework.routers import DefaultRouter

from .views import PostViewSet, GroupViewSet, CommentViewSet

# Роутер для запросов к группам, постам и комментариям в блоге.
router = DefaultRouter()
router.register(r'groups', GroupViewSet, basename='group')
router.register(r'posts', PostViewSet, basename='post')
router.register(r'posts/(?P<post_id>[^/.]+)/comments',
                CommentViewSet,
                basename='comment')

urlpatterns = [
    # Путь для получения существующим пользователем токена.
    path('api-token-auth/', views.obtain_auth_token),
    path('', include(router.urls)),
]
