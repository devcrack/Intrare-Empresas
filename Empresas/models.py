from django.db import models
from django.conf import settings


class Empresa(models.Model):
    custom_user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )
    name = models.CharField(
        max_length=100,
        unique=True, null=False,
        blank=False, name='name'
    )
    address = models.CharField(
        max_length=200,
        null=False,
        blank=False,
        name='address'
    )
    telephone = models.IntegerField(
        unique=True,
        null=False, blank=False,
        name='telephone'
    )
    email = models.EmailField(
        max_length=100, unique=True,
        null=False, blank=False,
        name='email'
    )
    logo = models.CharField(
        max_length=200,
        null=False,
        blank=False,
        name='logo'
    )
    web_page = models.CharField(
        max_length=100, null=False,
        blank=False
    )
    scian = models.IntegerField(
        null=False,
        blank=False, name='scian'
    )
    classification = models.CharField(
        max_length=100, null=False,
        blank=False, name='classification'
    )
    latitude = models.FloatField(
        null=False,
        blank=False,
        name='latitude'
    )
    longitude = models.FloatField(
        null=False, blank=False,
        name='longitude'
    )
    url_map = models.CharField(
        max_length=200, null=False,
        blank=False, name='url_map'
    )
    validity = models.DateField(null=False, blank=False, name='validity')

    def __str__(self):
        return self.name


class Administrador(models.Model):
    id_empresa = models.ForeignKey('Empresa', on_delete=models.CASCADE)
    id_usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def __str__(self):
        return self.id_usuario.username

    class Meta:
        verbose_name_plural = "Administradores"


class Empleado(models.Model):
    id_empresa = models.ForeignKey('Empresa', on_delete=models.CASCADE)
    id_usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    id_area = models.ForeignKey('Area', on_delete=models.CASCADE)
    extension = models.CharField(max_length=10, null=False, blank=False)
    puede_enviar = models.BooleanField(null=False, blank=False)
    id_notificaciones = models.CharField(max_length=100, null=False, blank=False)
    codigo = models.CharField(max_length=20, null=False, blank=False)

    def __str__(self):
        return self.id_usuario.username

    class Meta:
        verbose_name_plural = "Empleados"


class Vigilante(models.Model):
    id_empresa = models.ForeignKey('Empresa', on_delete=models.CASCADE)
    id_usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def __str__(self):
        return self.id_usuario.username

    class Meta:
        verbose_name_plural = "Vigilantes"


class Area(models.Model):
    id_empresa = models.ForeignKey('Empresa', on_delete=models.CASCADE)
    nombre = models.CharField(max_length=100, unique=True, null=False, blank=False)
    color = models.CharField(max_length=7, unique=True, null=False, blank=False)

    def __str__(self):
        return self.nombre


class Caseta(models.Model):
    id_empresa = models.ForeignKey('Empresa', on_delete=models.CASCADE)
    nombre = models.CharField(max_length=100, null=False, blank=False)
    activa = models.BooleanField(null=False, blank=False)

    def __str__(self):
        return self.nombre


class Veto(models.Model):
    id_empresa = models.ForeignKey('Empresa', on_delete=models.CASCADE)
    id_usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    fecha_hora_veto = models.DateTimeField(auto_now=False, auto_now_add=True, null=False)
    motivo = models.TextField(null=False, blank=False)
    tipo = models.CharField(max_length=45, null=False, blank=False)

    def __str__(self):
        return self.id_usuario.username


class Acceso(models.Model):
    id_empresa = models.ForeignKey('Empresa', on_delete=models.CASCADE)
    id_empleado = models.ForeignKey('Empleado', on_delete=models.CASCADE)
    id_invitacion = models.ForeignKey('Invitaciones.Invitacion', on_delete=models.CASCADE)
    id_vigilante_ent = models.ForeignKey('Vigilante', on_delete=models.CASCADE, related_name='entrada')
    id_vigilante_sal = models.ForeignKey('Vigilante', on_delete=models.CASCADE, related_name='salida')
    id_area = models.ForeignKey('Area', on_delete=models.CASCADE)
    fecha_hora_acceso = models.DateTimeField(null=False, blank=False)
    fecha_hora_salida = models.DateTimeField(null=False, blank=False)
    estado = models.CharField(max_length=45, null=False, blank=False)
    pase_salida = models.CharField(max_length=50, null=False, blank=False)
    motivo_no_firma = models.TextField(null=False, blank=False)
    comentarios_VE = models.TextField(null=False, blank=False)
    datos_coche = models.TextField(null=False, blank=False)
    equipo = models.TextField(null=False, blank=False)

    def __str__(self):
        return self.id_empleado.id_usuario.username
