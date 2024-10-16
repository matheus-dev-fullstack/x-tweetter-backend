from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .viewsets import PostViewSet, ImagemViewSet, LikeViewSet, CommentViewSet

router = DefaultRouter()
router.register(r'posts', PostViewSet, basename="posts")
router.register(r'imagens', ImagemViewSet, basename="imagens")
router.register(r'likes', LikeViewSet, basename="likes")
router.register(r'comentarios', CommentViewSet, basename="comentarios")

urlpatterns = [
    path("", include(router.urls)),
]