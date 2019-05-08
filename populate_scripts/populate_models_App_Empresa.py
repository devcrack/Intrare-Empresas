import os
import django
import random

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ControlAccs.settings')
django.setup()

from Empresas.models import  *
from Usuarios.models import CustomUser, Perfil
from faker import Faker


faker = Faker()

def add_vigilante():
    """Se agrega un determinado numero de registros a la tabla Vigilante.

    Args:
        N(int):Por default son 10 registro pero en realidad puede tomar el valor que le sea proporcionado.


    Todo:
        * Primero que nada se tiene que dar de alta un usuario.
        * Al dar de alta un usario como vigilante hay que tener especial cuidado de los campos
          que vamos a dar de alta para dicho registro.
        * Una vez que se haya creado el usuario hay que vincularlo con el vigilante.
        * Los vigilantes siempre se consideran como agentes externos a la empresa(Empresa de seguridad) ??,
          o en caso de ser vigilantes de la empresa, PASAN A ser EMPLEADOS????.
    """
    a_length = len(Empresa.objects.all())
    if a_length > 1:
        # Obtenemos un registro de la tabla empresa para vincularla con el vigilante  a generar.
        _empresa = Empresa.objects.all()[random.randint(1, a_length - 1)]
        _id_empresa = _empresa.id
        #Generemos un usuario que sera el vigilante, NO ES SUPER USARIO
        _user = add_user(False)
        #Se tiene que cargar que el perfil del usuario recien creado es un empleado.
        _perfil = Perfil.objects.get_or_create(id=_user.user_perfil.id)
        _perfil.es_empleado = True
        #Se tiene que cargar el numero telefonico del Guardia en Perfil.
        _perfil.celular = faker().msisdn()
        _perfil.save()
        _vigilante = Vigilante.objects.get_or_create(id_empresa=_empresa)

    else:
        print('Agrega registro a la tabla empresas\nNANI\n')
        return 0

def add_user(_is_superuser):
    full_name = faker.name()
    list = full_name.split()
    name = list[0] # Requiere: Vigalante,
    last_name = list[1] # Requiere: Vigiliante
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

