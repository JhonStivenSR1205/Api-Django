from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from core import views

router = DefaultRouter()
router.register(r'usuarios', views.UsuariosViewSet, basename='usuarios')
router.register(r'preferencias', views.PreferenciasUsuarioViewSet, basename='preferencias')
router.register(r'rutinas', views.RutinasActivasViewSet, basename='rutinas')
router.register(r'metricas', views.MetricaFisicaViewSet, basename='metricas')
router.register(r'calorias', views.RegistroCaloriasViewSet, basename='calorias')
router.register(r'ejercicios', views.EjerciciosViewSet, basename='ejercicios')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/auth/registro/', views.RegistroUsuarioView.as_view(), name='registro_usuario'),
    path('api/v1/auth/login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/v1/auth/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/v1/', include(router.urls)),
]