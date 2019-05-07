# -*- coding: utf-8 -*-
"""Modelos para las invitaciones.


Aqui creamos los modelos correspondientes para cada una de las tablas que comprende esta aplicacion
"""
from django.db import models

from django.conf import settings


class Invitacion(models.Model):
    """Clase en la que se apoya el modelo para la creacion de la tabla invitacion.


        Attributes:
             id_empresa(int): Identificador unico de la empresa, llave foranea.
             id_area(int): Identificador unico del area, llave foranea.
             id_empleado(int): Identificador unico del usuario, llave foranea.
             id_usuario(int): Identificador unico del area, llave foranea.
             fecha_hora_envio(DateTimeField): Fechar hora de envio de la invitacion.
             asunto(str): Argumento que justifica la visita.
             automovil(bool): Indica si el vistante, tiene o no un automovil.
             notas(str): Notas y comentario extras acerca de la visita.
             empresa(str):Nombre de la empresa o institucion de donde proviene el visitante.
             leida(bool): Bandera que indica si la invitacion ha sido leida o no, pero porquien(La empresa o el invitado)?.

    """
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
    """Clase en la que se apoya el modelo para la creacion de la tabla invitacion temporal.
    ¿Porque aqui no es importante que el invitado temporal no se le marque como leida la invitacion?


        Attributes:
             id_empresa(int): Identificador unico de la empresa, llave foranea.
             id_area(int): Identificador unico del area, llave foranea.
             id_empleado(int): Identificador unico del usuario, llave foranea.
             celular_invitado(str): Numero de telefono del invitado temporal.
             fecha_hora_envio(DateTimeField): Fechar hora de envio de la invitacion.
             asunto(str): Argumento que justifica la visita.
             automovil(bool): Indica si el vistante, tiene o no un automovil.
             notas(str): Notas y comentario extras acerca de la visita.
             empresa(str):Nombre de la empresa o institucion de donde proviene el visitante.

    """
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
    """Clase en la que se apoya el modelo para la creacion de la tabla invitacion temporal.
    ¿Porque aqui no es importante que el invitado temporal no se le marque como leida la invitacion?


        Attributes:
            id_empresa(int): Identificador unico de la empresa, llave foranea.
            id_area(int): Identificador unico del area, llave foranea.
            id_empleado(int): Identificador unico del usuario, llave foranea.
            id_usuario(int): Identificador unico del area, llave foranea.
            id_invitacion_temporal(int): Identificador unico de la invitacion temporal, llave foranea.
            email(str):email del invitado empresarial.
            fecha_hora_envio(DateTimeField): Fecha y hora de envio de la invitacion.
            fecha_hora_invitacion(DateTimeField): Fecha y hora a suscitar  la invitacion.
            asunto(str): Argumento que justifica la visita.
            automovil(bool): Indica si el vistante, tiene o no un automovil.
            notas(str): Notas y comentario extras acerca de la visita.
            empresa(str):Nombre de la empresa o institucion de donde proviene el visitante.
            asignada(bool):Este campo no lo entiendo del todo?.
            cod_seguridad(str): Constraseña especial?
        Todo:
            * Aque se refiere el campo asignada?
            * ¿cod_seguridad es una especie de contraseña?
    """


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
    """ Esto esta me lo puedo traer desde la consulta con el id_empresa??"""
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
    """Se refiere al equipo de seguridad que cada invitado pudiese llevar.


    Attributes:
        nombre(str): Nombre del equipo de seguridad.
    """
    nombre = models.CharField(max_length=254, null=False, blank=False)


    def __str__(self):        
        return f"No {self.id}"

    class Meta:
        verbose_name_plural = "Equipos de Seguridad"

class EquiposporInvitacion(models.Model):
    """Se refiere a los equipo de seguridad que cada invitado pudiese llevar.


    Attributes:
        id_equipo_seguridad(int): Clave foranea, que vincula con la tabla equipo seguridad.
        id_invitacion(int):
    """
    id_equipo_seguridad = models.ForeignKey('EquipoSeguridad', on_delete=models.CASCADE)
    id_invitacion = models.ForeignKey('Invitacion', on_delete=models.CASCADE)
    

    def __str__(self):        
        return f"No {self.id}"

    class Meta:
        verbose_name_plural = "Equipo por Invitaciones"


class EquipoporInvitacionesEmpresariales(models.Model):
    """Equipo de seguridad por cada invitacion empresarial.

    Attributes:
        id_equipo_seguridad(int): Clave foranea para hacer la vinculacion con la tabla equipo de seguridad.
        id_invitacion_empresarial: Clave foranea para hacer la vinculacion con la tabla de Invitacion Empresarial.
    """


    id_equipo_seguridad = models.ForeignKey('EquipoSeguridad', on_delete=models.CASCADE)
    id_invitacion_empresarial = models.ForeignKey('InvitacionEmpresarial', on_delete=models.CASCADE)


    def __str__(self):        
        return f"No {self.id}"

    class Meta:
        verbose_name_plural = "Equipo por Invitaciones Empresariales"


class EquipoporInvitacionTemporal(models.Model):
    """Equipo por asignado por cada invitacion temporal.


    Attributes:
        id_equipo_seguridad(int): Clave foranea para hacer la vinculacion con la tabla equipo de seguridad.
        id_invitacion_temporal: Clave foranea para hacer la vinculacion con la tabla de Invitacion Temporal.
    """
    id_equipo_seguridad = models.ForeignKey('EquipoSeguridad', on_delete=models.CASCADE)
    id_invitacion_temporal = models.ForeignKey('InvitacionTemporal', on_delete=models.CASCADE)


    def __str__(self):        
        return f"No {self.id}"


    class Meta:
        verbose_name_plural = "Equipo por Invitaciones Temporales"

