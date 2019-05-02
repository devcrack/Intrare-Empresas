from django.db import models
from django.conf import settings
from django.utils import timezone


class Parque(models.Model):
    nombre = models.CharField(max_length=150, blank=False, null=False, name='nombre')
    direccion = models.CharField(max_length=150, blank=False, null=False, name='direccion')
    telefono = models.CharField(max_length=15, blank=False, null=False, name='telefono')
    email = models.EmailField(blank=False, null=False)
    password = models.CharField(max_length=150, blank=False, null=False, name='password')

    def __str__(self):
        return self.nombre

    class Meta:
        verbose_name_plural = 'Parques'


class VigilanteParque(models.Model):
    id_parque = models.ForeignKey('Parque', on_delete=models.CASCADE)
    nombre_completo = models.CharField(max_length=200, blank=False, null=False,
                                       name='nombre_completo')
    celular = models.CharField(max_length=30, blank=False, null=False, name='celular')
    password = models.CharField(max_length=128, blank=False, null=False, name='password')
    activo = models.BooleanField()

    def __str__(self):
        return self.nombre_completo

    class Meta:
        verbose_name_plural = 'Vigilantes del Parque'


class AccesoParque(models.Model):
    id_parque = models.ForeignKey('Parque', on_delete=models.CASCADE)
    id_empresa = models.ForeignKey('Empresas.Empresa', on_delete=models.CASCADE)
    id_invitacion = models.ForeignKey('Invitaciones.Invitacion', on_delete=models.CASCADE)
    id_usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    id_vigilante_parqueEnt = models.ForeignKey('Empresas.Vigilante', on_delete=models.CASCADE, related_name='p_entrada')
    id_vigilante_parqueSal = models.ForeignKey('Empresas.Vigilante', on_delete=models.CASCADE, related_name='p_salida')
    fecha_hora_acceso = models.DateTimeField(default=timezone.now)
    fecha_hora_Salida = models.DateTimeField(auto_now=True)
    comentarios = models.CharField(max_length=45, blank=False, null=False, name='comentarios')

    def __str__(self):
        return self.id_empresa.name + self.id_usuario.username

    class Meta:
        verbose_name_plural = 'Accesos al Parque'




