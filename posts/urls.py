from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .viewsets import PostViewSet, ImagemViewSet, LikeViewSet, CommentViewSet
from django.conf import settings
from django.conf.urls.static import static


router = DefaultRouter()
router.register(r'posts', PostViewSet, basename="posts")
router.register(r'imagens', ImagemViewSet, basename="imagens")
router.register(r'likes', LikeViewSet, basename="likes")
router.register(r'comentarios', CommentViewSet, basename="comentarios")

urlpatterns = [
    path("", include(router.urls)),
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)