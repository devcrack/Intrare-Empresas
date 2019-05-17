from django.db import models
from Empresas.models import Empleado

class Grupo(models.Model):
    id_empleado = models.ForeignKey('Empresas.Empleado', on_delete=models.CASCADE)
    nombre = models.CharField(max_length=100, null=False, blank=False)

    def __str__(self):
        return self.nombre


class Contacto(models.Model):
    id_empleado = models.ForeignKey('Empresas.Empleado', on_delete=models.CASCADE)
    nombre = models.CharField(max_length=200, null=False, blank=False)
    email = models.EmailField(max_length=300, unique=True, null=False, blank=False)
    telefono = models.CharField(max_length=15, unique=True, null=False, blank=False)

    def __str__(self):
        return self.nombre

class Grupo_has_contacto(models.Model):
    id_grupo = models.ForeignKey('Grupo', on_delete=models.CASCADE)
    id_contacto = models.ForeignKey('Contacto', on_delete=models.CASCADE)

    def __str__(self):
        return self.id_grupo.nombre + " - " + self.id_contacto.nombre