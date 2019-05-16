from django.db import models
from django.contrib.auth.models import AbstractUser


class CustomUser(AbstractUser):
    """
    Clase que extiende de la clase User de django esta nos permite agregar uno o varios campo a User pero
    manteniendo la integridad de la original...
    Mas información:
        https://docs.djangoproject.com/en/2.2/topics/auth/customizing/#extending-django-s-default-user
    """
    #user_perfil = models.ForeignKey('Perfil', on_delete=models.CASCADE, related_name='perfil_user_perfil')

    """
    Perfil
    """
    celular = models.CharField(max_length=30, unique=True, null=False, blank=True, name='celular')
    ine_frente = models.CharField(max_length=25, null=False, blank=True, name='ine_frente')
    ine_atras = models.CharField(max_length=25, null=False, blank=True, name='ine_atras')
    roll = models.IntegerField(null=False, default=0, blank=True, name='roll') #DOCUMENTAR ESTO
    plataforma = models.CharField(max_length=25, default='', name='plataforma')  # Tipo de aplicacion que es el sistema(Web, Android, iOs)
    """
    Para que no haya problemas al momento de crear un nuevo usuario se crea su perfil y se le asigna :D.
    Esto se logra sobreescribiendo el método de Save..
    Este metodo solo es para que funcione createsuperuser, con DRF se crea primero el modelo de perfil y se le asigna
    al usuario todo estó mediante la vista.
    """
    # def save(self, *args, **kwargs):
    #
    #     if not hasattr(self, 'user_perfil'):
    #         p = Perfil(celular=str(self.username)+' - no number',
    #                    ine_frente='na', ine_atras='na', es_empleado=False, plataforma='na')
    #         p.save()
    #         self.user_perfil = p
    #     super().save(*args, **kwargs)


class Perfil(models.Model):
    """
    Clase que define el modelo perfil
    """
    celular = models.CharField(max_length=30, unique=True, null=False, blank=False, name='celular')
    ine_frente = models.CharField(max_length=25, null=False, blank=False, name='ine_frente')
    ine_atras = models.CharField(max_length=25, null=False, blank=False, name='ine_atras')
    es_empleado = models.BooleanField(name='es_empleado')
    plataforma = models.CharField(max_length=25, name='plataforma') #Tipo de aplicacion que es el sistema(Web, Android, iOs)

    def __str__(self):
        return self.celular

    class Meta:
        verbose_name_plural = "Perfiles"

