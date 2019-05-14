import os
from faker import Faker
import random
import django
from django.core.exceptions import ObjectDoesNotExist

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ControlAccs.settings')
django.setup()

from Invitaciones.models import *
from Empresas.models import Empresa, Area, Empleado
from Usuarios.models import CustomUser,Perfil


faker = Faker()


def add_Invitaciones(N=10):
    """Se agrega un determinado numero de registros a la tabla Invitaciones.

    Args:
        N(int):Por default son 10 registro pero en realidad puede tomar un valor que le sea proporcionado.

    Attributes:

    Todo:
        * Se tiene que obtener la empresa con la que se tiene que vincular, la invitacion.
        * Obtener el area vinculada con la empresa y la invitacion.
        * Obtenemos el empleado vinculado con la empresa que es quien genera la invitacion.
        * Generamos el usuario al que le esta asiganda la invitacion.
        * Finalmente se genera la invitacion.
    """

    a_length = len(Empresa.objects.all())
    if a_length > 1:
        # Obtenemos un registro de la tabla empresa para vincularla con las invitaciones a generar.
        _empresa = Empresa.objects.all()[random.randint(1, a_length - 1)]

        _id_empresa = _empresa.id
        # Obtenemos el area de la empresa con la que actualmente se esta trabajando, para generar la invitacion.
        try:
            _area_empresa = Area.objects.get(id=_id_empresa)
        except ObjectDoesNotExist:
            print("Agrega Areas vinculadas a la empresa con este Id" + str(_id_empresa) + "\n")
            return 0
        # Obtenemos el empleado que pertenece a esta empresa, es decir quien genero la invitacion
        try:
            _empleado = Empleado.objects.get(_id_empresa)
        except ObjectDoesNotExist:
            print("Agrega Areas empleados a la empresa con este Id" + str(_id_empresa) + "\n")
            return 0
        length_user_records = len (CustomUser.objects.all())
        if length_user_records > 1:
            for entry in range(N):
                # Obtenemos un usuario random al que le asignaremos una invitacion creada.
                _usuario = CustomUser.objects.all()[random.randint(1, length_user_records)]
                _fecha_hora_envio = faker.date_time()
                _fecha_hora_invitacion = faker.date_time()
                _asunto = faker.paragraph(max_nb_chars=250, ext_word_list=None)
                _automovil = bool(random.getrandbits(1))
                _notas = faker.paragraph(max_nb_chars=150, ext_word_list=None)
                _Empresa = faker.company()
                _leida = bool(random.getrandbits(1))
                invitacion = Invitacion.objects.get_or_create(
                    id_empresa=_empresa, id_area=_area_empresa,
                    id_empleado=_empleado, id_usuario=_usuario,
                    fecha_hora_envio=_fecha_hora_envio,
                    fecha_hora_invitacion=_fecha_hora_invitacion,
                    asunto=_asunto, automovil=_automovil,
                    notas=_notas, empresa=_empresa,
                    leida=_leida
                )
                invitacion.save()

        else:
            print("Agrega usuarios no administradores a esta empresa" + str(_id_empresa) + "\n")
            return 0
    else:
        print('Agrega registro a la tabla empresas\nNANI\n')
        return 0


def add_InvitacionTemporal(N=10):
    """Se agrega un determinado numero de registros a la tabla InvitacionTemporal.

        Args:
            N(int):Por default son 10 registro pero en realidad puede tomar un valor que le sea proporcionado.

        Attributes:

        Todo:
            * Se tiene que obtener la empresa con la que se tiene que vincular, la invitacion.
            * Obtener el area vinculada con la empresa y la invitacion.
            * Obtener el empleado vinculado con la empresa que es quien genera la invitacion.
            * Generamos el usuario al que le esta asiganda la invitacion.
            * Finalmente se genera la invitacion.
        """
    a_length = len(Empresa.objects.all())
    if a_length > 1:
        # Obtenemos un registro de la tabla empresa para vincularla con las invitaciones a generar.
        _empresa = Empresa.objects.all()[random.randint(1, a_length - 1)]
        _id_empresa = _empresa.id
        # Obtenemos el area de la empresa con la que actualmente se esta trabajando, para generar la invitacion.
        try:
            _area_empresa = Area.objects.get(id=_id_empresa)
        except ObjectDoesNotExist:
            print("Agrega Areas vinculadas a la empresa con este Id" + str(_id_empresa) + "\n")
            return 0
            # Obtenemos el empleado que pertenece a esta empresa, es decir quien genero la invitacion
        try:
            _empleado = Empleado.objects.get(_id_empresa)
        except ObjectDoesNotExist:
            print("Agrega Areas empleados a la empresa con este Id" + str(_id_empresa) + "\n")
            return 0
        for entry in range(N):
            # Obtenemos un usuario random al que le asignaremos una invitacion creada.
            _celular_invitado = faker().msisdn()
            _fecha_hora_envio = faker.date_time()
            _fecha_hora_invitacion = faker.date_time()
            _asunto = faker.paragraph(max_nb_chars=250, ext_word_list=None)
            _automovil = bool(random.getrandbits(1))
            _notas = faker.paragraph(max_nb_chars=150, ext_word_list=None)
            _empresa = faker.company()
            invitacion_temp = InvitacionTemporal.objects.get_or_create(
                id_empresa=_id_empresa, id_area=_area_empresa,
                id_empleado=_empleado, celular_invitado=_celular_invitado,
                fecha_hora_envio=_fecha_hora_envio, fecha_hora_invitacion=_fecha_hora_invitacion,
                asunto=_asunto, automovil=_automovil,
                notas=_notas, empresa=_empresa
            )[0]
            invitacion_temp.save()
    else:
        print('Agrega registro a la tabla empresas\nNANI\n')
        return 0



def add_invitacion_Empresarial():
    """Se agrega un registro a la tabla usuarios.

            Args:
                N(int):Por default son 10 registro pero en realidad puede tomar un valor que le sea proporcionado.

            Attributes:

            Todo:
                * Se tiene que obtener la empresa con la que se tiene que vincular, la invitacion.
                * Obtener el area vinculada con la empresa y la invitacion.
                * Obtener el empleado vinculado con la empresa que es quien genera la invitacion.
                * Generamos el usuario al que le esta asiganda la invitacion.
                * Finalmente se genera la invitacion.
            """
    a_length = len(Empresa.objects.all())
    if a_length > 1:
        # Obtenemos un registro de la tabla empresa para vincularla con las invitaciones a generar.
        _empresa = Empresa.objects.all()[random.randi(1, a_length - 1)]
        _id_empresa = _empresa.id
        # Obtenemos el area de la empresa con la que actualmente se esta trabajando, para generar la invitacion.
        try:
            _area_empresa = Area.objects.get(id=_id_empresa)
        except ObjectDoesNotExist:
            print("Agrega Areas vinculadas a la empresa con este Id" + str(_id_empresa) + "\n")
            return 0
        # Obtenemos el empleado que pertenece a esta empresa, es decir quien genero la invitacion
        try:
            _empleado = Empleado.objects.get(_id_empresa)
        except ObjectDoesNotExist:
            print("Agrega Areas empleados a la empresa con este Id" + str(_id_empresa) + "\n")
            return 0
        # Creamos un usuario para vincularlo a esta invitacion temporal
        _user = add_user(False)
        _perfil = Perfil.objects.get_or_create(id=_user.user_perfil.id)
        _perfil.es_empleado = False
        _perfil.celular = faker().msisdn()
        _perfil.save()
        invitacion_Empresarial = InvitacionEmpresarial(
            id_empresa=_empresa, id_area=_area_empresa,
            id_empleado=_empleado, id_usuario=_user,

        )
    else:
        print('Agrega registro a la tabla empresas\nNANI\n')
        return 0


def add_user(_is_superuser):
    full_name = faker.name()
    list = full_name.split()
    name = list[0]  # Requiere: Vigalante,
    last_name = list[1]  # Requiere: Vigiliante
    email = faker.email()
    username_pre = email.split("@")
    username = username_pre[0]
    password = faker.password()
    is_staff = False
    is_active = True
    is_superuser = _is_superuser
    last_login = faker.date_time()
    user = CustomUser.objects.get_or_create(
        first_name=name,
        last_name=last_name,
        username=username,
        email=email,
        is_staff=is_staff,
        is_active=is_active,
        is_superuser=is_superuser,
        last_login=last_login,
        password=password)[0]
    user.save()

    return user

def add_equipo_seguridad():
    fake_name = faker.job()
    equipo_seguridad = EquipoSeguridad(nombre=fake_name)


