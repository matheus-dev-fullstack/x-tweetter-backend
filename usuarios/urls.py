from django.urls import path, include
from rest_framework.routers import DefaultRouter

from usuarios.viewsets import LoginViewSet, RegisterViewSet, PerfilViewSet
from django.conf import settings
from django.conf.urls.static import static

# login_list = LoginViewSet.as_viewset({'post': 'authenticate'})

router = DefaultRouter()
router.register(r'registrar', RegisterViewSet, basename="registrar")
router.register(r'perfil', PerfilViewSet, basename="perfil")
# router.register(r'login', LoginViewSet, basename="login")
    # path('auth/login/', LoginViewSet.as_view({'post': 'authenticate'}), name='login'),


urlpatterns = [
    path('login/', LoginViewSet.as_view({'post': 'authenticate'}), name='login'),
    path('', include(router.urls)),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
# urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
# urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# if settings.DEBUG:
#     urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)