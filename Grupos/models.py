from django.db import models
from Empresas.models import Empleado

from django.conf import settings


class Grupo(models.Model):
    """
    Modelo Grupo:

    Representa la Tabla Grupo en la Base de Datos.

    Attributes:
        id_empleado(int): ID del Empleado el cuál creó el Grupo.
        nombre(str): Nombre del Grupo.

    """
    id_usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    nombre = models.CharField(max_length=100, null=False, blank=False)

    def __str__(self):
        return self.nombre


class Grupo_has_contacto(models.Model):
    """
    Modelo Grupo_has_contacto:

    Representa la Tabla Grupo_has_contacto en la Base de Datos.

    Attributes:

        id_grupo(int): ID del Grupo.
        id_cotacto(int): ID del Contacto.
    """
    id_grupo = models.ForeignKey('Grupo', on_delete=models.CASCADE)
    id_contacto = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def __str__(self):
        return self.id_grupo.nombre + " - " + self.id_contacto.first_name