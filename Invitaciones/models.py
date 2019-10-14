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
    fecha_hora_envio = models.DateTimeField(default=timezone.datetime.now, null=False, blank=False)
    typeInv = models.IntegerField(default=0, null=False)  # 0=Inv Normal, 1=Recurrente 2= Referidos
    dateInv = models.DateField(null=False) #
    timeInv = models.TimeField(null=False) #
    diary = models.CharField(max_length=7, default="")  # Dias de la semana que asistira recurrentemente LMXJVSD
    asunto = models.CharField(max_length=254, null=False, blank=False)
    automovil = models.BooleanField(null=False, blank=False)
    notas = models.CharField(max_length=256, null=True, blank=True, default="")
    empresa = models.CharField(max_length=254, null=True, blank=True, default="")
    leida = models.BooleanField(default=False, null=False)

    def __str__(self):
        return f"ID_Invitation: {self.id}   ;  COMPANY: {self.empresa};"

    # def save(self, *args, **kwargs):
    #     code = token_hex(8)
    #     self.qr_code = code
    #     super(Invitacion, self).save(*args, **kwargs)

    class Meta:
        verbose_name_plural = "INVITACIONES"


class InvitationByUsers(models.Model):
    idInvitation = models.ForeignKey('Invitacion', on_delete=models.CASCADE, null=False, related_name='InvitationLINK') # Esta instancia puede tener muchas invitaciones
    qr_code = models.CharField(max_length=30, null=False)
    host = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, default=None, related_name='Invitation_host')
    idGuest = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=False, related_name='Invitation_guest')

    def __str__(self):
        return f"ID = {self.id} QRCode {self.qr_code} INV:{self.idInvitation}  GUEST = {self.idGuest}"

    class Meta:
        verbose_name_plural = "UsersByInvitation"


class ReferredInvitation(models.Model):
    referredMail = models.EmailField(default=None, null=True)
    referredPhone = models.CharField(default=None, max_length=12, null=True)
    qrCode = models.CharField(max_length=14, null=False, blank=True, unique=True)
    referredExpiration = models.DateField(null=False, blank=False)
    maxForwarding = models.IntegerField(default=3)
    host = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, default=None,
                             related_name='InvitationReferred_host')

    def __str__(self):
        return f"ID={self.id} HOST{self.host} Referido: {self.referredMail} Expiracion: {self.referredExpiration}"
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
