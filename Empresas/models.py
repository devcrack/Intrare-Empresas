from django.db import models
from django.conf import settings


class Empresa(models.Model):
    """Modelo Empresa

       Representa la tabla Empresa en la Base de Datos.

       Attributes:
            name(str): Nombre de la Empresa.
            address(str): Dirección de la Empresa.
            telephone(str): Teléfono de la Empresa.
            email(email): Dirección de Correo Electrónico de la Empresa.
            logo(str): Ubicación del archivo logo de la Empresa.
            web_page(str): Direccón de la Página Web de la Empresa.
            scian(int): Código Sistema de Clasificación
                        Industrial de América del Norte de la Empresa.
            classification(str): Clasificación de la Empresa.
            latitude(float): Latitud de la Empresa.
            longitude(float): Longitud de la Empresa.
            url_map(str): Dirección web del mapa de la Empresa.
            validity(Date): Vigencia de la Empresa.
    """
    # custom_user = models.OneToOneField(
    #     settings.AUTH_USER_MODEL,
    #     on_delete=models.CASCADE
    # )
    id_parque = models.ForeignKey(
    'Parques.Parque',
    on_delete=models.CASCADE,
    default=None,
    null=True

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
    telephone = models.CharField(
        max_length=30,
        unique=True,
        null=False,
        blank=True,
        name='telephone')
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
        return self.id_usuario.username

    class Meta:
        verbose_name_plural = "Administradores"


class Empleado(models.Model):
    """
    Modelo Empleado  name(str): Nombre de la Empresa.
            address(str): Dirección de la Empresa.
            telephone(str): Teléfono de la Empresa.
            email(email): Dirección de Correo Electrónico de la Empresa.
            logo(str): Ubicación del archivo logo de la Empresa.
            web_page(str): Direccón de la Página Web de la Empresa.
            scian(int): Código Sistema de Clasificación
                        Industrial de América del Norte de la Empresa.
            classification(str): Clasificación de la Empresa.
            latitude(float): Latitud de la Empresa.
            longitude(float): Longitud de la Empresa.
            url_map(str): Dirección web del mapa de la Empresa.
            validity(Date): Vigencia de la Empresa.

    Represnta la Tabla Empleado
    en la Base de Datos.

    Attributes:
        id_empresa(int): ID de la Empresa al cual pertenece el Empleado,
        id_usuario(int):ID del Usaurio del Empĺeado.
        id_area(int): ID del Area al cual pertenece el Empleado.
        extension(str): Extensión del Usuario
        puede_enviar(bool): Bandera para saber si el Empleado puede eviar invitaciones:
                        True: Puede enviar invitaciones.
                        False:NO puede enviar invitaciones.
        id_notificaciones(): Identificador de la Notificación.
        codigo(): Código QR.

    Todo:
        * para que se ocupa el atributo extension?


    """
    id_empresa = models.ForeignKey('Empresa', on_delete=models.CASCADE)
    id_usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    id_area = models.ForeignKey('Area', on_delete=models.CASCADE)
    extension = models.CharField(max_length=10, null=False, blank=False)
    puede_enviar = models.BooleanField(null=False, blank=False)
    id_notificaciones = models.CharField(max_length=100, null=False, blank=False)
    codigo = models.CharField(max_length=20, null=False, blank=False)

    def __str__(self):
        """
        Método que devuelve el nombre de usuario
        del Empleado
        :return: id_usuario.username
        """
        # return self.id_usuario.username
        return f"EMPLOYEE->{self.id}; User->{self.id_usuario.id}{self.id_usuario.first_name} {self.id_usuario.last_name}; Company->{self.id_empresa.name}"
    class Meta:
        verbose_name_plural = "Empleados"


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
    """
    Modelo Veto.

    Representa la Tabla Veto en la Base de Datos.

    Attributes:
        id_empresa(int): ID de la Empresa en la cual está registrado
                         el Usuario .
        id_usuario(int): ID del Usuario al cual se va vetar.
        fecha_hora_veto(DateTime): Fecha y Hora en el que se vetó al Usuario.
        motivo(str): Motivo por el cual se vetó al Usuario.
        tipo(str):

        Todo:
            * que tipos de Vetos hay?
    """
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
    """
    Modelo Acceso.

    Representa la Tabla Acceso en la Base de Datos.

    Attributes:
        id_empresa(int): ID de la Empresa el cual registra el Acceso.
        id_empleado(int): ID  del Empleado al cual se dá Acceso.
        id_invitacion(int): ID Invitación
        id_vigilante_ent(int): ID del vigilante que registró la entrada.
        id_vigilante_sal(int): ID del vigilante que registró la salida.
        estado(str):
        pase_salida(str)
        motivo_no_firma(str): Motivo por el cuál no firmó el Acceso.
        comentarios_VE(str): Comentarios adicionales del Vigilante.
        datos_coche(str): Datos adicionales del Coche.
        equipo(str): Equipo necesario para el Acceso:
                        Zapatos Especilaes
                        Casco
                        etc.

        Todo:
            * para que se emplea el atributo pase_salida??? R:
            * para que se emplea el atributo estado??? R:
            * El empleado es quien genera el acceso??? R:
            * Acceso esta vinculada con una invitacion, cuando se le concede acceso el campo de
              leida  a esa invitacion se pone en TRUE?, y eso indica que el acceso ya ha sido concedido?
            * El acceso lo puede conceder el empleado y/o el vigilante? EL ACCESO SIEMRE LO TIENE DAR EL VIGILANTE.
            * ¿A que se refiere con vigilante Entrada, Vigilante Salida?, ¿Puede ser alguno de estos campos
                                                                           Nulo, si es que el acceso se lo concedio
                                                                           un empleado? NO.

    """
    id_empresa = models.ForeignKey('Empresa', on_delete=models.CASCADE)
    id_empleado = models.ForeignKey('Empleado', on_delete=models.CASCADE)
    id_invitacion = models.ForeignKey('Invitaciones.Invitacion', on_delete=models.CASCADE)
    id_vigilante_ent = models.ForeignKey('Vigilante', on_delete=models.CASCADE, related_name='entrada')
    id_vigilante_sal = models.ForeignKey('Vigilante', on_delete=models.CASCADE, related_name='salida')
    id_area = models.ForeignKey('Area', on_delete=models.CASCADE)
    fecha_hora_acceso = models.DateTimeField(null=False, blank=False)
    fecha_hora_salida = models.DateTimeField(null=False, blank=False)
    estado = models.CharField(max_length=45, null=False, blank=False)
    pase_salida = models.CharField(max_length=50, null=False, blank=False)# Check que valida que se ha efectuado la visita, ya se con el empleado o con el amdinistrador.
    motivo_no_firma = models.TextField(null=False, blank=False)
    comentarios_VE = models.TextField(null=False, blank=False)
    datos_coche = models.TextField(null=False, blank=False)
    equipo = models.TextField(null=False, blank=False)

    def __str__(self):
        """
        Método que retorna el nombre de usuario.
        :return: id_empleado.id_usuario.username
        """
        return self.id_empleado.id_usuario.username
