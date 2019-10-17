# -*- coding: utf-8 -*-
from django.db import models

from django.conf import settings
from secrets import token_hex
from django.utils import timezone
from datetime import date


def defaultExpiration():
    _year = timezone.datetime.now().year
    _month = timezone.datetime.now().month
    _day = timezone.datetime.now().day
    _date = date(_year, _month, _day)

    _delta = timezone.timedelta(days=1)

    return _date + _delta

    """
    Codigo de soporte
    """
    # return date(_year, _month, _day)
    # # _DateExp = fecha_hora_envio.get_default()
    #
    # _delta = timezone.timedelta(days=1)
    # _DateExp = _DateExp + _delta
    # dateInv = models.DateField(default=_DateExp, null=False)
    # timeInv = models.TimeField(default=time(), null=False)
    # # _DateExp = dateInv.get_default()
    # # _delta = timezone.timedelta(days=2)
    # # _DateExp = _DateExp + _delta
    # expiration = models.DateField(default=dateInv, null=False)
    # _DateExp = dateInv.get_default()
    # _delta = timezone.timedelta(days=2)
    # _DateExp = _DateExp + _delta
    # expiration = models.DateField(default=_DateExp, null=False)


class Invitacion(models.Model):
    """Clase en la que se apoya el modelo para la creacion de la tabla invitacion.
    """

    id_empresa = models.ForeignKey('Empresas.Empresa', on_delete=models.CASCADE, related_name='id_company_inv')
    id_area = models.ForeignKey('Empresas.Area', on_delete=models.CASCADE, blank=False, null=False)
    fecha_hora_envio = models.DateTimeField(default=timezone.datetime.now, null=False, blank=False)
    typeInv = models.IntegerField(default=0, null=False)  # 0=Inv Normal, 1=Recurrente 2= Referidos
    dateInv = models.DateField(null=False) #
    timeInv = models.TimeField(null=False) #
    expiration = models.DateField(default=defaultExpiration())
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
    # Campos Necesarios para generar la invitacion Intrinseca
    id_empresa = models.ForeignKey('Empresas.Empresa', on_delete=models.CASCADE, related_name='id_company_ReferredInv') # No Editable
    areaId = models.ForeignKey('Empresas.Area', on_delete=models.CASCADE, blank=False, null=False)  # No editable
    fecha_hora_envio = models.DateTimeField(default=timezone.datetime.now, null=False, blank=False)
    dateInv = models.DateField(null=False)  # No Editable
    timeInv = models.TimeField(null=False)  # No Editable
    expiration = models.DateField(default=defaultExpiration())
    diary = models.CharField(max_length=7, default="")  # No Editable
    subject = models.CharField(max_length=254, null=False, blank=False) #No Editable
    vehicle = models.BooleanField(null=False, blank=False)
    notes = models.CharField(max_length=256, null=True, blank=True, default="")
    companyFrom = models.CharField(max_length=254, null=True, blank=True, default="") #No Editable
    host = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, default=None,
                             related_name='InvitationReferred_host')
    Token = models.CharField(max_length=14, default=token_hex(7))  # No Editable
    referredMail = models.EmailField(default=None, null=False)
    referredPhone = models.CharField(default=None, max_length=12, null=True)

    def __str__(self):
        return f"ID{self.id} HOST_{self.host} COMPANY_FROM : {self.companyFrom} GUESTEMAIL: {self.referredMail}"

    class Meta:
        verbose_name_plural = "EnterpriseInvitation"


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
