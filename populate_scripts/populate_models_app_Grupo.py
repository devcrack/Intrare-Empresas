import os
from faker import Faker
import random
import django
from django.core.exceptions import ObjectDoesNotExist

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ControlAccs.settings')
django.setup()

from Grupos.models import *
from Empresas.models import Empleado
from .random_numbers import phn

faker = Faker()


def add_group(n=5):
    """
    Función  para agregar N Grupos(registros)
    en la Base de Datos de la Tabla Grupo.
    Nota: Se debe agregar registros a la Tabla Empleado
    antes de usar esta función.
    :param n: Número de registros Grupo a agregar por Empleado
    """
    count_employees = len(Empleado.objects.all())
    if count_employees > 0:
        for i in range(n):
            a_employe = Empleado.objects.all()[random.randint(1, count_employees - 1)]
            faker_name = faker.country()
            group = Grupo.objects.get_or_create(
                nombre=faker_name,
                id_empleado=a_employe
            )[0]
            group.save()
    else:
        print('You must to add some Employees first!!!')


def add_contact(n=5):
    """
    Función para Agregar un registro Contacto aleatoriamente a un Empleado
    a la Base de Datos a la Tabla Contacto.
    Nota: Se debe agregar registros a la Tabla Empleado
    antes de usar esta función.
    :param n: Número de registros Contacto a agregar.
    """
    count_employees = len(Empleado.objects.all())
    if count_employees > 0:
        for i in range(n):
            a_employee = Empleado.objects.all()[random.randint(1, count_employees - 1)]
            faker_name = faker.name()
            faker_email = faker.email()
            faker_telefono = phn()
            a_contact = Contacto.objects.get_or_create(
                id_empleado=a_employee,
                nombre=faker_name,
                email=faker_email,
                telefono=faker_telefono
            )[0]
            a_contact.save()
    else:
        print('You must add some Employees first!!!')
    pass


def add_group_has_contact(n=5):
    """
    Función para agregar N registros a la Base de Datos
    de la Tabla Grupo_has_contacto.
    Nota: para poblar esta Tabla de debe de dar de alta
    registros en la Tabla Grupo y Contacto.
    :param n: Número de registros a agregar.
    :return:
    """
    count_contacts = len(Contacto.objects.all())
    if count_contacts > 0:
        count_group = len(Grupo.objects.all())
        if count_group > 0:
            for i in range(n):
                a_contact = Contacto.objects.all()[random.randint(0, count_contacts - 1)]
                a_group = Grupo.objects.all()[random.randint(0, count_group - 1)]
                a_group_has_contact = Grupo_has_contacto.objects.get_or_create(
                    id_contacto=a_contact,
                    id_grupo=a_group
                )[0]
                a_group_has_contact.save()
        else:
            print('You must add some Groups, first!!!')
    else:
        print('You must add some Contacts first!!!')