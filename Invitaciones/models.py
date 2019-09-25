# -*- coding: utf-8 -*-
from django.db import models

from django.conf import settings
from secrets import token_hex
from datetime import datetime, date, time
from django.utils import timezone
import qrcode


class Invitacion(models.Model):
    """Clase en la que se apoya el modelo para la creacion de la tabla invitacion.
    """

    id_empresa = models.ForeignKey('Empresas.Empresa', on_delete=models.CASCADE, related_name='id_company_inv')
    id_area = models.ForeignKey('Empresas.Area', on_delete=models.CASCADE, blank=False, null=False)
    id_admin = models.ForeignKey('Empresas.Administrador', on_delete=models.CASCADE, blank=True, null=True)  # Anfitrion T1
    id_empleado = models.ForeignKey('Empresas.Empleado', on_delete=models.CASCADE, blank=True, null=True) #Anfitrion T2
    id_usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, default=None)
    _defSent = timezone.now()
    fecha_hora_envio = models.DateTimeField(default=_defSent, null=False, blank=False)
    typeInv = models.IntegerField(default=0, null=False)  # 0=Inv Normal, 1=Recurrente 2= Referidos
    dateInv = models.DateField(default=date(year=timezone.now().year, month=timezone.now().month, day=timezone.now().day+1), null = False)
    timeInv = models.TimeField(default=time(), null=False)
    # _DateExp = dateInv.get_default()
    # _delta = timezone.timedelta(days=2)
    # _DateExp = _DateExp + _delta
    expiration = models.DateField(default=dateInv, null=False)
    #Pendiente
    diary = models.CharField(max_length=7, default="")  # Dias de la semana que asistira recurrentemente LMXJVSD

    asunto = models.CharField(max_length=254, null=False, blank=False)
    automovil = models.BooleanField(null=False, blank=False)
    notas = models.CharField(max_length=256, null=True, blank=True, default="")
    empresa = models.CharField(max_length=254, null=True, blank=True, default="")
    leida = models.BooleanField(default=False, null=False)
    qr_code = models.CharField(max_length=16, null=False, blank=True, unique=True)

    def __str__(self):
        return f"ID_Invitation: {self.id};  COMPANY: {self.empresa}; GUEST_PHONE: " \
            f"{self.id_usuario.celular}; GUEST:MAIL: {self.id_usuario.email}"

    def save(self, *args, **kwargs):
        code = token_hex(8)
        self.qr_code = code
        super(Invitacion, self).save(*args, **kwargs)

    class Meta:
        verbose_name_plural = "INVITACIONES"


class InvitacionReferido(models.Model):
    idInvitacion = models.ForeignKey('Invitacion', on_delete=models.CASCADE)
    emailTercero = models.EmailField(null=False, blank=False)
    asignada = models.BooleanField(null=False, blank=False, default=False)
    hashCode = models.CharField(max_length=100, null=False, unique=True)

    def __str__(self):
        return f"ID = {self.id}-EmailTercer{self.emailTercero}  Invitacion = {self.idInvitacion}"
        #return "%s %s" % (str(self.id), self.email)


    class Meta:
        verbose_name_plural = "InvitacionesReferido"

class EquipoSeguridad(models.Model):
    """Se refiere al equipo de seguridad que cada invitado pudiese llevar.


    Attributes:
        nombre(str): Nombre del equipo de seguridad.
    """
    nombre = models.CharField(max_length=254, null=False, blank=False, unique=True)

    def __str__(self):
        return f"ID->{self.id} NAME:{self.nombre}"

    class Meta:
        verbose_name_plural = "EquipoSeguridad"


class EquiposporInvitacion(models.Model):
    """Se refiere a los equipo de seguridad que cada invitado pudiese llevar.

    Attributes:
        id_equipo_seguridad(int): Clave foranea, que vincula con la tabla equipo seguridad.
        id_invitacion(int):
    """
    id_equipo_seguridad = models.ForeignKey('EquipoSeguridad', on_delete=models.CASCADE)
    id_invitacion = models.ForeignKey('Invitacion', on_delete=models.CASCADE)
    

    def __str__(self):        
        return f"Invitation->{self.id_invitacion.id} Security Equipment:{self.id_equipo_seguridad.nombre}"

    class Meta:
        verbose_name_plural = "Security Equipment by Invitation"
