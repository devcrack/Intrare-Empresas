import django
import os
from faker import Faker
from django.core.exceptions import ObjectDoesNotExist
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ControlAccs.settings')
django.setup()
from Usuarios.models import CustomUser
from Empresas.models import *
from Invitaciones.models import *
from Parques.models import *
from .random_numbers import *



faker = Faker()


def addSimpleUser(*args):
    """
    args:
        args[0] : Register number wished.
        args[1]: email.
        args[2]: password.
    """
    _nReg = args[0]
    for i in range(_nReg):
        _name = faker.name()
        _email = unique_id() + args[1]
        _password = args[2]
        username_pre = _email.split("@")
        _username = username_pre[0] + unique_id()
        _cellphone = phn()
        _list = _name.split()
        _firstName = _list[0]
        _lastName = _list[1]
        
        user = CustomUser.objects.create_user(first_name=_firstName, last_name=_lastName, username=_username, email=_email,
                                         password=_password, celular=_cellphone)
        # user.save()
        print('USER CREATED wit mail  =')
        print(_email)
        print(' And Password  =')
        print(_password)


def add_user(_is_superuser, type_rol):
    """Creates a non Staff User.
    Args:
        _is_superuser : Indicates if user will be super user.
        type_rol: Type Rol that the user going have.
    """
    full_name = faker.name()
    list = full_name.split()
    name = list[0]
    last_name = list[1]
    email = faker.email()
    username_pre = email.split("@")
    username = username_pre[0] + unique_id()
    password = faker.password()
    is_staff = False
    is_active = True
    is_superuser = _is_superuser
    _cellphone = phn()
    _rol = type_rol
    # last_login = faker.date_time()
    user = CustomUser.objects.create_user(
        first_name=name,
        last_name=last_name,
        username=username,
        email=email,
        is_staff=is_staff,
        is_active=is_active,
        is_superuser=is_superuser,
        # last_login=last_login,
        password=password,
        celular=_cellphone,
        roll=_rol
        )
    user.save()
    print('USER CREATED\n')
    return user


def add_user1(*args):
    """Creates a non Staff User.
    Args:
        args:Tuple that contains all parameters.
        args[0](bool):Indicates if user will be super user.
        args[1](int): Type Rol that the user going have.
        args[2](str): email of user.
        args[3](str): Password.
    """

    full_name = faker.name()
    _email = unique_id() + args[2]
    password = args[3]
    list = full_name.split()
    name = list[0]
    last_name = list[1]
    username_pre = _email.split("@")
    username = username_pre[0] + unique_id()
    is_staff = False
    is_active = True
    is_superuser = args[0]
    _cellphone = phn()
    _rol = args[1]
    # last_login = faker.date_time()
    user = CustomUser.objects.create_user(
        first_name=name,
        last_name=last_name,
        username=username,
        email=_email,
        is_staff=is_staff,
        is_active=is_active,
        is_superuser=is_superuser,
        # last_login=last_login,
        password=password,
        celular=_cellphone,
        roll=_rol
        )
    print('USER CREATED wit mail  =')
    print(_email)
    print(' And Password  =')
    print(password)

    return user


def print_dummy_message():
    print('Hello from populate_scripts/__init__.py\n')