from django.utils import timezone
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .models import (
    Usuarios,
    MetricaFisica,
    RegistroCalorias,
    RutinasActivas,
    Ejercicios
)
from .serializers import (
    RutinasActivasSerializer,
    MetricaFisicaSerializer,
    RegistroCaloriasSerializer,
    EjerciciosSerializer
)


def obtener_usuario_fitlive(user):
    """
    Busca o crea automáticamente el usuario en SQL Server 
    cuando llega la petición autenticada por JWT.
    """
    usuario_bd, created = Usuarios.objects.get_or_create(
        identificador=user.username,
        defaults={
            'nombre': user.username,
            'correo': user.email or f"{user.username}@fitlive.com",
            'clave_hash': user.password,
            'rol': 'cliente',
            'esta_activo': True,
            'fecha_registro': timezone.now(),
        }
    )
    return usuario_bd


class RutinasActivasViewSet(viewsets.ModelViewSet):
    queryset = RutinasActivas.objects.all().order_by('-id_rutina')
    serializer_class = RutinasActivasSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        usuario_bd = obtener_usuario_fitlive(self.request.user)
        serializer.save(id_usuario=usuario_bd)


class MetricaFisicaViewSet(viewsets.ModelViewSet):
    queryset = MetricaFisica.objects.all().order_by('-id_metrica')
    serializer_class = MetricaFisicaSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        usuario_bd = obtener_usuario_fitlive(self.request.user)
        serializer.save(id_usuario=usuario_bd)


class RegistroCaloriasViewSet(viewsets.ModelViewSet):
    queryset = RegistroCalorias.objects.all().order_by('-id_caloria')
    serializer_class = RegistroCaloriasSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        usuario_bd = obtener_usuario_fitlive(self.request.user)
        serializer.save(id_usuario=usuario_bd)


class EjerciciosViewSet(viewsets.ModelViewSet):
    queryset = Ejercicios.objects.all().order_by('id_ejercicio')
    serializer_class = EjerciciosSerializer
    permission_classes = [IsAuthenticated]