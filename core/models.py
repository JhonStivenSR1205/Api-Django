from django.db import models
from decimal import Decimal


class Usuarios(models.Model):
    id_usuario = models.AutoField(primary_key=True)
    identificador = models.CharField(unique=True, max_length=50, db_collation='Modern_Spanish_CI_AS')
    nombre = models.CharField(max_length=150, db_collation='Modern_Spanish_CI_AS')
    correo = models.CharField(unique=True, max_length=150, db_collation='Modern_Spanish_CI_AS')
    clave_hash = models.CharField(max_length=255, db_collation='Modern_Spanish_CI_AS')
    rol = models.CharField(max_length=20, default='usuario', db_collation='Modern_Spanish_CI_AS')
    esta_activo = models.BooleanField(default=True)
    fecha_registro = models.DateTimeField(auto_now_add=True)

    class Meta:
        managed = False
        db_table = 'usuarios'

    def __str__(self):
        return self.nombre


class PreferenciasUsuario(models.Model):
    id_preferencia = models.AutoField(primary_key=True)
    id_usuario = models.OneToOneField(Usuarios, models.CASCADE, db_column='id_usuario')
    tema_visual = models.CharField(max_length=20, default='claro', db_collation='Modern_Spanish_CI_AS')
    recibir_notificaciones = models.BooleanField(default=True)

    class Meta:
        managed = False
        db_table = 'preferencias_usuario'


class MetricaFisica(models.Model):
    id_metrica = models.AutoField(primary_key=True)
    id_usuario = models.ForeignKey(Usuarios, models.CASCADE, db_column='id_usuario')
    peso = models.DecimalField(max_digits=5, decimal_places=2)
    estatura = models.DecimalField(max_digits=4, decimal_places=2)
    imc = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    fecha_registro = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        # Calcula automáticamente el IMC antes de guardar en SQL Server
        if self.peso and self.estatura and Decimal(self.estatura) > 0:
            self.imc = round(Decimal(self.peso) / (Decimal(self.estatura) ** 2), 2)
        super().save(*args, **kwargs)

    class Meta:
        managed = False
        db_table = 'metrica_fisica'


class RegistroCalorias(models.Model):
    id_caloria = models.AutoField(primary_key=True)
    id_usuario = models.ForeignKey(Usuarios, models.CASCADE, db_column='id_usuario')
    alimento = models.CharField(max_length=150, db_collation='Modern_Spanish_CI_AS')
    calorias = models.DecimalField(max_digits=7, decimal_places=2)
    fecha_registro = models.DateField(auto_now_add=True)

    class Meta:
        managed = False
        db_table = 'registro_calorias'


class RutinasActivas(models.Model):
    id_rutina = models.AutoField(primary_key=True)
    id_usuario = models.ForeignKey(Usuarios, models.CASCADE, db_column='id_usuario')
    nombre_rutina = models.CharField(max_length=100, db_collation='Modern_Spanish_CI_AS')
    fecha_programada = models.DateField(auto_now_add=True)
    completada = models.BooleanField(default=False)

    class Meta:
        managed = False
        db_table = 'rutinas_activas'

    def __str__(self):
        return self.nombre_rutina


class Ejercicios(models.Model):
    id_ejercicio = models.AutoField(primary_key=True)
    id_rutina = models.ForeignKey(
        RutinasActivas,
        models.CASCADE,
        db_column='id_rutina',
        related_name='ejercicios'
    )
    nombre_ejercicio = models.CharField(max_length=120, db_collation='Modern_Spanish_CI_AS')
    series = models.IntegerField()
    repeticiones = models.IntegerField()
    completado = models.BooleanField(default=False)

    class Meta:
        managed = False
        db_table = 'ejercicios'