from django.db import models
from django.conf import settings
from django.utils import timezone

class Empresa(models.Model):
    id_parque = models.ForeignKey('Parques.Parque', on_delete=models.CASCADE, default=None, null=True)
    name = models.CharField(max_length=100, unique=True, null=False, blank=False, name='name')
    address = models.CharField(max_length=200, null=False, blank=False, name='address')
    telephone = models.CharField(max_length=30, unique=True, null=False, blank=True, name='telephone')
    email = models.EmailField(max_length=100, unique=True, null=False, blank=False, name='email')
    logo = models.ImageField(upload_to="Logos", max_length=256, blank=False, null=False, default=None)
    web_page = models.CharField(max_length=100, null=False, blank=False)
    scian = models.IntegerField(null=False, blank=False, name='scian')
    classification = models.CharField(max_length=100, null=False, blank=False, name='classification')
    latitude = models.FloatField(null=False, blank=False, name='latitude')
    longitude = models.FloatField(null=False, blank=False, name='longitude')
    url_map = models.CharField(max_length=200, null=False, blank=False, name='url_map')
    validity = models.DateField(null=False, blank=False, name='validity')
    enabled = models.BooleanField(default=True)


    def __str__(self):
        """
        Método que devuelve el nombre de la Empresa
        :return: name
        """
        # return self.name
        return f"ID->{self.id}; Company: {self.name}"

class Administrador(models.Model):
    """
        Modelo Administrador

        Represnta la Tabla Administrador
        en la Base de Datos.

        Attributes:
            id_empresa(int): ID de la Empresa en la cual está registrado
                             el Administrador.
            id_usuario(int): ID del Usuario del Administrador.
    """
    id_empresa = models.ForeignKey('Empresa', on_delete=models.CASCADE)
    id_usuario = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def __str__(self):
        """
        Método que devuelve en nombre de usuario del Administrador
        :return: id_usuario.username
        """
        return f"ADMIN->{self.id}; User->{self.id_usuario.id}{self.id_usuario.first_name} {self.id_usuario.last_name}; Company->{self.id_empresa.name}"

    class Meta:
        verbose_name_plural = "Administradores"


class Empleado(models.Model):

    id_empresa = models.ForeignKey('Empresa', on_delete=models.CASCADE)
    id_usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    id_area = models.ForeignKey('Area', on_delete=models.CASCADE)
    extension = models.CharField(max_length=10, null=False, blank=False)
    puede_enviar = models.BooleanField(null=False, blank=False, default=True)
    def __str__(self):
        """
        Método que devuelve el nombre de usuario
        del Empleado
        :return: id_usuario.username
        """
        # return self.id_usuario.username
        return f"EMPLOYEE->{self.id}; User->{self.id_usuario.id}{self.id_usuario.first_name} {self.id_usuario.last_name}; Company->{self.id_empresa.name}"
    class Meta:
        verbose_name_plural = "Employee"


class Vigilante(models.Model):
    """
    Modelo Vigilante

    Representa la Tabla Vigilante en la Base de Datos.


    Attributes:
        id_empresa(int): ID de la Empresa en la cual está registrado
                         el Vigilante.
        id_usuario(int): ID del Usuario del Vigilante.

    """
    id_empresa = models.ForeignKey('Empresa', on_delete=models.CASCADE)
    id_usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def __str__(self):
        """
        Método que devuelve el nombre de usuario del Vigilante
        :return:id_usuario.username
        """
        return self.id_usuario.username

    class Meta:
        verbose_name_plural = "Vigilantes"


class Area(models.Model):
    """
    Modelo Area

    Representa la Tabla Area en la Base de Datos.

    Attributes:
        id_empresa(int): ID de la Empresa en la cual está registrado
                         el Área.
        name(str): Nombre del Área.
        color(str): Color para identificar el Área.
    """
    id_empresa = models.ForeignKey('Empresa', on_delete=models.CASCADE)
    nombre = models.CharField(max_length=100, null=False, blank=False)
    color = models.CharField(max_length=7, null=False, blank=False)

    def __str__(self):
        """
        Método que devuelve el nombre de la Empresa y su Área
        :return: id_empresa.name + nombre
        """
        return f"ID->{self.id}; NAME:{self.nombre}; Company:{self.id_empresa.name}"


class Caseta(models.Model):
    """
    Modelo Caseta

    Represnta la Tabla Caseta en la Base de Datos.

    Attributes:
        id_empresa(int): ID de la Empresa en la cual está registrado
                         la Caseta.
         nombre(str): Nombre de la Caseta.
         activa(bool): Bandera para saber si la Caseta está vigente:
                        True: Aún sigue vigente.
                        False: Esta desactivada.

    """
    id_empresa = models.ForeignKey('Empresa', on_delete=models.CASCADE)
    nombre = models.CharField(max_length=100, null=False, blank=False)
    activa = models.BooleanField(null=False, blank=False)

    def __str__(self):
        """
        Método qwe retorna el nombre de la Caseta.
        :return:
        """
        return self.nombre+ " - " +  self.id_empresa.name


class Veto(models.Model):
    id_empresa = models.ForeignKey('Empresa', on_delete=models.CASCADE)
    id_usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    fecha_hora_veto = models.DateTimeField(auto_now=False, auto_now_add=True, null=False)
    motivo = models.TextField(null=False, blank=False)
    tipo = models.CharField(max_length=45, null=False, blank=False)

    def __str__(self):
        """
        Método que retorna el nombre del usuario.
        :return: id_usuario.username.
        """
        return self.id_usuario.username


class Acceso(models.Model):
    invitationByUsers = models.ForeignKey('Invitaciones.InvitationByUsers', on_delete=models.CASCADE)
    id_vigilante_ent = models.ForeignKey('Vigilante', on_delete=models.SET_NULL, null=True,related_name='Ventrada',
                                         default=None)
    id_vigilante_sal = models.ForeignKey('Vigilante', on_delete=models.SET_NULL, related_name='Viglantesalida',
                                         blank=True, null=True, default=None)
    fecha_hora_acceso = models.DateTimeField(default=timezone.datetime.now, null=False, blank=False)  # Automaticamente se genera al crear el registro
    fecha_hora_salida = models.DateTimeField(default=None, null=True, blank=True)  # Temporalmente esta vacio, posteriormente se actualizara el terminar la visita.
    estado = models.IntegerField(default=1, null=False, blank=False)  # 1 = Entrada, 2 = Salida
    pase_salida = models.BooleanField(default=False, null=False, blank=True)  # Check que valida que se ha efectuado la visita, ya sea con el empleado o con el amdinistrador.
    motivo_no_firma = models.TextField(null=True, blank=True , max_length=400)  # Este campo es utilizado en caso de que el pase de salida se mantenga en False.
    comentarios_VE = models.TextField(null=True, blank=True, max_length=300)  # No siempre se da el caso de haber comentarios.
    datos_coche = models.TextField(null=True, blank=True)  # No siempre el visitante trae un coche
    equipo = models.TextField(null=True, blank=True, default=None)
    qr_code = models.CharField(max_length=30, null=False, blank=False, unique=True)  # Para no hacer una doble consulta y evitar estresar la base de datos.

    def __str__(self):
        """
        Método que retorna el nombre de usuario.
        :return: id_empleado.id_usuario.username
        """
        return f'Id_Acc={self.id} qrCode:{self.qr_code}'

class SecurityEquipment(models.Model):
    """Se refiere al equipo de seguridad que cada invitado pudiese llevar.


    Attributes:
        nombre(str): Nombre del equipo de seguridad.
    """
    nameEquipment = models.CharField(max_length=254, null=False, blank=False, unique=False)
    idArea = models.ForeignKey(Area, on_delete=models.CASCADE, default=None, related_name="SecurityEquipmentByArea")

    def __str__(self):
        return f"ID->{self.id} NAME:{self.nameEquipment}, AREA:{self.idArea}"

    class Meta:
        verbose_name_plural = "Equipment Security"

