from rest_framework import serializers
from .models import (
    Usuarios,
    PreferenciasUsuario,
    MetricaFisica,
    RegistroCalorias,
    RutinasActivas,
    Ejercicios
)


class EjerciciosSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(source='id_ejercicio', read_only=True)

    class Meta:
        model = Ejercicios
        fields = ['id', 'id_rutina', 'nombre_ejercicio', 'series', 'repeticiones', 'completado']


class RutinasActivasSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(source='id_rutina', read_only=True)
    usuario = serializers.IntegerField(source='id_usuario.id_usuario', read_only=True)
    usuario_nombre = serializers.CharField(source='id_usuario.nombre', read_only=True)
    ejercicios = EjerciciosSerializer(many=True, read_only=True)

    class Meta:
        model = RutinasActivas
        fields = [
            'id',
            'usuario',
            'usuario_nombre',
            'nombre_rutina',
            'fecha_programada',
            'completada',
            'ejercicios'
        ]


class MetricaFisicaSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(source='id_metrica', read_only=True)
    usuario = serializers.IntegerField(source='id_usuario.id_usuario', read_only=True)
    usuario_nombre = serializers.CharField(source='id_usuario.nombre', read_only=True)
    imc = serializers.FloatField(read_only=True)

    class Meta:
        model = MetricaFisica
        fields = [
            'id',
            'usuario',
            'usuario_nombre',
            'peso',
            'estatura',
            'imc',
            'fecha_registro'
        ]


class RegistroCaloriasSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(source='id_caloria', read_only=True)
    usuario = serializers.IntegerField(source='id_usuario.id_usuario', read_only=True)
    usuario_nombre = serializers.CharField(source='id_usuario.nombre', read_only=True)

    class Meta:
        model = RegistroCalorias
        fields = ['id', 'usuario', 'usuario_nombre', 'alimento', 'calorias', 'fecha_registro']