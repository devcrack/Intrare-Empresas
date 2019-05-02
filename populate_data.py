from faker import Faker
import os
import django
import random
from Empresas.models import Empresa
from Usuarios.models import CustomUser


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ControlAccs.settings')
django.setup()

fake_generator = Faker()
CustomUser.objects.cr

""" Generamos una lista de empresas X """
empresas = ['Red Sparrow', 'Tecnopal', 'Imparable', 'Nearsfot', 'Lanimfe', 'Softek']

""" Funcion que nos genera una Empresa X """
#def add_Empresa():
#    fake
#    _E = Empresa.objects.get_or_create(name=random.choice(empresas))
