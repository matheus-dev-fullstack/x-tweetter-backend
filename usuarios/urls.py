from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .viewsets import UsuarioViewSet
from django.conf import settings
from django.conf.urls.static import static


router = DefaultRouter()
router.register(r'usuarios', UsuarioViewSet, basename="usuarios")

urlpatterns = router.urls

# urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
# urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# if settings.DEBUG:
#     urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)