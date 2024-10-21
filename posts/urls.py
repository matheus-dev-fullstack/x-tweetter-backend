from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .viewsets import PostViewSet, ImagemViewSet, LikeViewSet, CommentViewSet
from django.conf import settings
from django.conf.urls.static import static
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

router = DefaultRouter()
router.register(r'posts', PostViewSet, basename="posts")
router.register(r'imagens', ImagemViewSet, basename="imagens")
router.register(r'likes', LikeViewSet, basename="likes")
router.register(r'comentarios', CommentViewSet, basename="comentarios")

urlpatterns = [
    path("", include(router.urls)),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)