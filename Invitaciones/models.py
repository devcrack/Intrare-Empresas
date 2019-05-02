from django.db import models

from django.conf import settings


class Invitacion(models.Model):
    id_empresa = models.ForeignKey('Empresas.Empresa', on_delete=models.CASCADE)
    id_area = models.ForeignKey('Empresas.Area', on_delete=models.CASCADE)
    id_empleado = models.ForeignKey('Empresas.Empleado', on_delete=models.CASCADE)
    id_usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    fecha_hora_envio = models.DateTimeField(null=False, blank=False)
    fecha_hora_invitacion = models.DateTimeField(null=False, blank=False)
    asunto = models.CharField(max_length=254, null=False, blank=False)
    automovil = models.BooleanField(null=False, blank=False)
    notas = models.CharField(max_length=12)
    """ Esto  me lo puedo traer desde la consulta con el id_empresa"""
    empresa = models.CharField(max_length=254, null=False, blank=False)
    leida =models.BooleanField(null=False, blank=False)

    def __str__(self):
        return "%s %s" % (str(self.id), self.id_usuario.email)

    class Meta:
        verbose_name_plural = "Invitaciones"

class InvitacionTemporal(models.Model):
    id_empresa = models.ForeignKey('Empresas.Empresa', on_delete=models.CASCADE)
    id_area = models.ForeignKey('Empresas.Area', on_delete=models.CASCADE)
    id_empleado = models.ForeignKey('Empresas.Empleado', on_delete=models.CASCADE)
    celular_invitado = models.CharField(max_length=13)
    fecha_hora_envio = models.DateTimeField(null=False, blank=False)
    fecha_hora_invitacion = models.DateTimeField(null=False, blank=False)
    asunto = models.CharField(max_length=254, blank=False)            
    automovil = models.BooleanField(null=False, blank=False)
    notas = models.CharField(max_length=254)       
    empresa = models.CharField(max_length=254, null=False,blank=False)    

 
class InvitacionEmpresarial(models.Model):
    id_empresa = models.ForeignKey('Empresas.Empresa', on_delete=models.CASCADE)
    id_area = models.ForeignKey('Empresas.Area', on_delete=models.CASCADE)
    id_empleado = models.ForeignKey('Empresas.Empleado', on_delete=models.CASCADE)
    id_usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    id_invitacion_temporal = models.ForeignKey('InvitacionTemporal', on_delete=models.CASCADE)    
    """ Necesita un validador para email """
    email = models.EmailField(max_length=100, unique=True, null=False, blank=False,name='email')
    fecha_hora_envio = models.DateTimeField(null=False, blank=False)
    fecha_hora_invitacion = models.DateTimeField(null=False, blank=False)    
    asunto = models.CharField(max_length=254, null=False, blank=False)
    automovil = models.BooleanField(null=False, blank=False)
    notas = models.CharField(max_length=12)
    """ Esto esta pendejo me lo puedo traer desde la consulta con el id_empresa"""
    empresa = models.CharField(max_length=254, null=False, blank=False)
    asignada = models.BooleanField(null=False, blank=False)
    """ Necesita un validador para contraseñas """
    cod_seguridad = models.CharField(max_length=254, null=False, blank=False)
    def __str__(self):
        return f"{self.id}-{self.email}"
        #return "%s %s" % (str(self.id), self.email)
    class Meta:
        verbose_name_plural = "Invitaciones Empresariales"


class EquipoSeguridad(models.Model):
    nombre = models.CharField(max_length=254, null=False, blank=False)


    def __str__(self):        
        return f"No {self.id}"

    class Meta:
        verbose_name_plural = "Equipos de Seguridad"

class EquiposporInvitacion(models.Model):    
    id_equipo_seguridad = models.ForeignKey('EquipoSeguridad', on_delete=models.CASCADE)
    id_invitacion = models.ForeignKey('Invitacion', on_delete=models.CASCADE)
    

    def __str__(self):        
        return f"No {self.id}"

    class Meta:
        verbose_name_plural = "Equipo por Invitaciones"


class EquipoporInvitacionesEmpresariales(models.Model):
    id_equipo_seguridad = models.ForeignKey('EquipoSeguridad', on_delete=models.CASCADE)
    id_invitacion_empresarial = models.ForeignKey('InvitacionEmpresarial', on_delete=models.CASCADE)


    def __str__(self):        
        return f"No {self.id}"

    class Meta:
        verbose_name_plural = "Equipo por Invitaciones Empresariales"


class EquipoporInvitacionTemporal(models.Model):
    id_equipo_seguridad = models.ForeignKey('EquipoSeguridad', on_delete=models.CASCADE)
    id_invitacion_temporal = models.ForeignKey('InvitacionTemporal', on_delete=models.CASCADE)


    def __str__(self):        
        return f"No {self.id}"


    class Meta:
        verbose_name_plural = "Equipo por Invitaciones Temporales"

