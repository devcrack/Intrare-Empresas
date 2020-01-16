from django.db import models
from datetime import datetime


class Bitacora(models.Model):
    id_vigilante = models.ForeignKey('Empresas.Vigilante', on_delete=models.CASCADE)
    id_caseta = models.ForeignKey('Empresas.Caseta', on_delete=models.CASCADE)
    id_empresa = models.ForeignKey('Empresas.Empresa', on_delete=models.CASCADE)
    id_empleado = models.ForeignKey('Empresas.Empleado', on_delete=models.CASCADE)
    id_area = models.ForeignKey('Empresas.Area', on_delete=models.CASCADE)
    f_acceso = models.DateTimeField(default=datetime.now, null=False, blank=False)
    f_salida = models.DateTimeField(default=None, null=True,blank=True)
    url_foto = models.ImageField(upload_to="WithoutAccess", max_length=256, blank=False, null=False, default=None)
    nombre = models.CharField(max_length=200, null=False,blank=False)
    telefono = models.CharField(max_length=20, null=False,blank=False)
    empresa = models.CharField(max_length=100, null=False,blank=False)
    notas = models.TextField(null=False, blank=False)

    def __str__(self):
        return self.nombre


class BitacoraEmpresarial(models.Model):
    id_vigilante = models.ForeignKey(
        'Empresas.Vigilante', 
        on_delete=models.CASCADE)
    id_emprea = models.ForeignKey(
        'Empresas.Empresa', 
        on_delete=models.CASCADE)
    id_empleado = models.ForeignKey(
        'Empresas.Empleado', 
        on_delete=models.CASCADE)
    f_acceso = models.DateTimeField(
        null=False, 
        blank=False)
    f_salida = models.DateTimeField(
        null=False, 
        blank=False)

    def __str__(self):
        return self.id_empleado.id_usuario.username    

    class Meta:
        verbose_name_plural = "Bitacoras Empresariales"