import os
import django
import random
from django.core.exceptions import ObjectDoesNotExist

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ControlAccs.settings')
django.setup()

from Parques.models import Parque
from faker import Faker

faker = Faker()


def add_parque(N=10):
    for entry in range(N):
        fake_parque = Parque.objects.get_or_create(
            nombre=faker.company(),
            direccion=faker.address(),
            telefono=faker.number(),
            email=faker.email(),
            password=faker.password()
        )
        fake_parque.save()
