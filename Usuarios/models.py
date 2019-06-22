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
    email = models.EmailField(unique=True, blank=True, name='email', null=True)
    celular = models.CharField(max_length=30, unique=True, null=False, blank=False, name='celular')
    ine_frente = models.CharField(max_length=25, default='', null=False, blank=True, name='ine_frente')
    ine_atras = models.CharField(max_length=25, default='', null=False, blank=True, name='ine_atras')
    roll = models.IntegerField(null=False, default=0, blank=False, name='roll')
    plataforma = models.CharField(max_length=25, default='', name='plataforma')  # Tipo de aplicacion que es el sistema(Web, Android, iOs)

    """
    Aqui se especifican los campos obligatorios para poder reegistrar un usuarios.
    
    y el campo que se utilizara para iniciar sesion
    """
    REQUIRED_FIELDS = ["celular", "username", "first_name", "last_name"]
    USERNAME_FIELD = "email"

    def __str__(self):
        return f"ID->{self.id}; Name: {self.first_name } {self.last_name}; Number_Phone{self.celular}; email: {self.email}; Roll={self.roll}"


