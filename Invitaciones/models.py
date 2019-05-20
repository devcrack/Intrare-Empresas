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
             leida(bool): Bandera que indica si la invitacion ha sido leida por el invitado.


    Todo:
         *Siempre el empleado genera la invitaciones
         * El campo empresa(STRING) que es el nombre de la empresa en la que se
           esta generando la invitacion?, o es la empresa de la que proviene el invitado?
           R: Es la empresa de donde viene el invitado, y puede estar vacio.
    """
    id_empresa = models.ForeignKey('Empresas.Empresa', on_delete=models.CASCADE)
    id_area = models.ForeignKey('Empresas.Area', on_delete=models.CASCADE)
    id_empleado = models.ForeignKey('Empresas.Empleado', on_delete=models.CASCADE)
    id_usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, default=None)
    fecha_hora_envio = models.DateTimeField(null=False, blank=False)
    fecha_hora_invitacion = models.DateTimeField(null=False, blank=False)
    asunto = models.CharField(max_length=254, null=False, blank=False)
    automovil = models.BooleanField(null=False, blank=False)
    notas = models.CharField(max_length=12)
    """ Esto  me lo puedo traer desde la consulta con el id_empresa"""
    empresa = models.CharField(max_length=254, null=False, blank=False)
    leida =models.BooleanField(null=False, blank=False) #  Se activa cuando el invitado revisa la invitacion y asi el empleado se de cuenta de que se ha leido.

    def __str__(self):
        return "%s %s" % (str(self.id), self.id_usuario.email)

    class Meta:
        verbose_name_plural = "Invitaciones"


        
class InvitacionTemporal(models.Model):
    """Clase en la que se apoya el modelo para la creacion de la tabla invitacion temporal.


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


    Todo:
        * ¿Exactamente que es una invitacion temporal? R: Es para aquellos que no estan registrados,
          posteriormente cuando se registren se cargara la informacion de la invitacion temporal, al usuario que se esta registrando  haciendo
          match mediante el numero de telefono.
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
    """Este tipo de invitacion es para aquellas entidades que tienen una invitacion a la empresa
    pero que se desconoce el usuario, es decir que el usuario no ha sido registrado, pero que mas
    sin embargo una empresa tiene asignada una invitacion.
    Clase en la que se apoya el modelo para la creacion de la tabla invitacion temporal.
    ¿Porque aqui no es importante que el invitado temporal no se le marque como leida la invitacion?


        Attributes:
            id_empresa(int): Id de la empresa a la que se va a visitar.
            id_area(int): Id del area de la empresa a la que se va a visitar.
            id_empleado(int): Id del empleado que genera la visita a la empresa.
            id_usuario(int): iD del usuario que va a visitar la empresa, PUEDE SER NULO.
            id_invitacion_temporal(int): ??????????
            email(str):email del invitado empresarial.
            fecha_hora_envio(DateTimeField): Fecha y hora de envio de la invitacion.
            fecha_hora_invitacion(DateTimeField): Fecha y hora a suscitar  la invitacion.
            asunto(str): Argumento que justifica la visita.
            automovil(bool): Indica si el vistante, tiene o no un automovil.
            notas(str): Notas y comentario extras acerca de la visita.
            empresa(str):Nombre de la empresa o institucion de donde proviene el visitante.
            asignada(bool):Este campo no lo entiendo del todo?.
            cod_seguridad(str): Constraseña especial,


        Todo:
            * Aque se refiere el campo asignada? R: Si esta asignada a un visitante???
            * ¿cod_seguridad es una especie de contraseña? R:truco para proteger la URL
            * El campo email, no se puede cubrir con el campo email, del usuario??? R: EMAIL del usuario que se desconoce
            * El campo empresa, ¿No lo puedo obtener mediante la interseccion de ID_Empresa? R: EMPRESIA DE DONDE PROVIENE EL VISITANTE
            * Los campos id_empresa., id_area, id_empleado,  en que difieren con los
              campos de la tabla INVITACION_TEMPORAL, ya que al parecer tienen los mismo campos?.
            R:
            * Que pasa con la invitacion Empresarial cuando si se conoce el usuario(Cuando se conoce
                                                                                   es porque esta dado de alta?)
              pasa a ser una invitacion normal?, ya que en un determinado momento la invitaicon  es una invitacion empresarial, pero si
              el usuario se da de alta o se vincula a esta invitacion empresarial, daria lugar a una invitacion normal?
            * email(str):email del invitado empresarial, Que pasa con este campo cuando si se conoce
                         cuando si hay un usuario registrado para vincularlo con esta invitacion.


    """


    id_empresa = models.ForeignKey(
        'Empresas.Empresa',
        on_delete=models.CASCADE,
        blank=False)
    id_area = models.ForeignKey(
        'Empresas.Area',
        on_delete=models.CASCADE,
        blank=False)
    id_empleado = models.ForeignKey(
        'Empresas.Empleado',
        on_delete=models.CASCADE,
        blank=False)
    id_usuario = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        blank=True,
        on_delete=models.CASCADE) # ESTO PUEDE SER NULL
    id_invitacion_temporal = models.ForeignKey(
        'InvitacionTemporal',
        on_delete=models.CASCADE,
    default=None)
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
    cod_seguridad = models.CharField(max_length=254, null=False, blank=False) #Truco para proteger la url


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

