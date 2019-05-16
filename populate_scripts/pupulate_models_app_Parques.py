import os
import django

import random
from django.core.exceptions import ObjectDoesNotExist

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ControlAccs.settings')
django.setup()

from django.conf import settings
from Parques.models import Parque, VigilanteParque, AdministradorParque
from faker import Faker
from Usuarios.models import CustomUser

faker = Faker()


def add_parque():
    fake_parque = Parque.objects.get_or_create(
        nombre=faker.company(),
        direccion=faker.address(),
    )
    fake_parque[0].save()
    return fake_parque[0]


def add_Parques(n=5):
    for i in range(n):
        fake_parque = add_parque()
        for n in range(2):
            user = add_user(settings.PAR_VIGILANTE)
            add_vigilantes(fake_parque, user)
        user = add_user(settings.ADMIN_PARQUE)
        add_admins(fake_parque, user)


def add_vigilantes(p, u):
    fake_v = VigilanteParque(
        id_parque=p,
        id_usuario=u
    )
    fake_v.save()


def add_admins(p, u):
    fake_ad = AdministradorParque(
        id_parque=p,
        id_usuario=u
    )
    fake_ad.save()


def add_user(roll):
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
    is_superuser = False
    last_login = faker.date_time()
    celular = str(faker.msisdn())
    roll = roll
    user = CustomUser.objects.get_or_create(
        first_name=name,
        last_name=last_name,
        username=username,
        email=email,
        is_staff=is_staff,
        is_active=is_active,
        is_superuser=is_superuser,
        last_login=last_login,
        password=password,
        celular=celular,
        roll=roll
    )[0]
    user.save()
    return user
