from django.db import models
from django.contrib.auth.models import AbstractUser


def nameFile(instance, filename):
    return '/'.join(['images', str(instance.username), filename])


class CustomUser(AbstractUser):
    """
    Clase que extiende de la clase User de django esta nos permite agregar uno o varios campo a User pero
    manteniendo la integridad de la original...
    Mas información:
        https://docs.djangoproject.com/en/2.2/topics/auth/customizing/#extending-django-s-default-user
    """
    """
    Perfil
    """
    email = models.EmailField(unique=True, blank=True, name='email', null=True)
    celular = models.CharField(max_length=30, unique=True, null=False, blank=False, name='celular')
    ine_frente = models.ImageField(upload_to=nameFile, max_length=256, blank=True, null=True, default=None)
    ine_atras = models.ImageField(upload_to=nameFile, max_length=256, blank=True, null=True, default=None)
    avatar = models.ImageField(upload_to=nameFile, max_length=256, blank=True, null=True, default="avatar.png")
    roll = models.IntegerField(null=False, default=0, blank=False, name='roll')
    temporalToken = models.CharField(max_length=8, default="", null=False, blank=True)
    plataforma = models.CharField(max_length=25, default='web', name='plataforma')  # Tipo de aplicacion que es el sistema(Web, Android, iOs)
    host = models.ForeignKey("self", null=True, on_delete=models.SET_NULL, related_name="anfitrion")  # Campo que ayuda a referenciar el anfitrion para este invitado.
    userSettings = models.OneToOneField('UserSettings', on_delete=models.CASCADE)

    """
    Aqui se especifican los campos obligatorios para poder reegistrar un usuarios.
    
    y el campo que se utilizara para iniciar sesion
    """
    REQUIRED_FIELDS = ["celular", "username", "first_name", "last_name"]
    USERNAME_FIELD = "email"
    def save(self, *args, **kwargs):
        print("que pasa")
        _nwSettings = UserSettings()
        _nwSettings.save()
        self.userSettings = _nwSettings
        super(CustomUser,self).save(*args, **kwargs)

    def __str__(self):
        return f"ID->{self.id}; Name: {self.first_name } {self.last_name}; Number_Phone{self.celular}; email: {self.email}; Roll={self.roll}"

class UserSettings(models.Model):
    canSendSmS = models.BooleanField(default=True)
    canSendEmail = models.BooleanField(default=True)
    language = models.CharField(max_length=3, default="esp")

    def __str__(self):
        return f"ID{self.id}"
