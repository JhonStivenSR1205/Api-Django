from django.utils import timezone
from django.contrib.auth.models import User
from rest_framework import viewsets, generics, status
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from .models import (
    Usuarios,
    PreferenciasUsuario,
    MetricaFisica,
    RegistroCalorias,
    RutinasActivas,
    Ejercicios
)
from .serializers import (
    UsuariosSerializer,
    PreferenciasUsuarioSerializer,
    RutinasActivasSerializer,
    MetricaFisicaSerializer,
    RegistroCaloriasSerializer,
    EjerciciosSerializer
)

def obtener_usuario_fitlive(user):
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

class RegistroUsuarioView(generics.CreateAPIView):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        username = request.data.get('username')
        password = request.data.get('password')
        email = request.data.get('email', f"{username}@fitlive.com")

        if not username or not password:
            return Response({"error": "Faltan usuario o contraseña"}, status=status.HTTP_400_BAD_REQUEST)

        if User.objects.filter(username=username).exists():
            return Response({"error": "El usuario ya existe"}, status=status.HTTP_400_BAD_REQUEST)

        User.objects.create_user(username=username, email=email, password=password)
        return Response({"mensaje": "Usuario creado exitosamente"}, status=status.HTTP_201_CREATED)

class UsuariosViewSet(viewsets.ModelViewSet):
    queryset = Usuarios.objects.all().order_by('-id_usuario')
    serializer_class = UsuariosSerializer
    permission_classes = [IsAuthenticated]

class PreferenciasUsuarioViewSet(viewsets.ModelViewSet):
    queryset = PreferenciasUsuario.objects.all().order_by('-id_preferencia')
    serializer_class = PreferenciasUsuarioSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        usuario_bd = obtener_usuario_fitlive(self.request.user)
        serializer.save(id_usuario=usuario_bd)

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