from django.urls import path, include
from rest_framework.routers import DefaultRouter

from usuarios.viewsets.usuario_viewset import LoginViewSet
from .viewsets import UsuarioViewSet
from django.conf import settings
from django.conf.urls.static import static

# login_list = LoginViewSet.as_viewset({'post': 'authenticate'})

router = DefaultRouter()
router.register(r'usuarios', UsuarioViewSet, basename="usuarios")
# router.register(r'login', LoginViewSet, basename="login")
    # path('auth/login/', LoginViewSet.as_view({'post': 'authenticate'}), name='login'),


urlpatterns = [
    path('login/', LoginViewSet.as_view({'post': 'authenticate'}), name='login'),
    path('', include(router.urls)),
]
# urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
# urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# if settings.DEBUG:
#     urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)