import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ControlAccs.settings')
import django
django.setup()

from Empresas.models import Caseta, Empresa
from faker import Faker

import random


#Posibles Nombres de Casetas
NAMES = [
    'Norte',
    'Sur',
    'Este',
    'Oeste'
]

obj = Faker()


def fill_caseta_table(N=5):
    num_empresas = len(Empresa.objects.all())
    if num_empresas > 1:
        for i in range(num_empresas - 1):
            a_company = Empresa.objects.all()[i]
            for j in range(0, 3):
                nombre = NAMES[j]
                num_random = random.randint(0, 1)
                if num_random == 0:
                    activa = False
                else:
                    activa = True
                caseta = Caseta.objects.get_or_create(
                    id_empresa=a_company,
                    nombre=nombre,
                    activa=activa
                )[0]
                caseta.save()
    else:
        print('You must to add some Companies first\n')

# if __name__ == '__main__':
#     print('Filling random data')
#     fill_table_area()
#     print('Filling Done!!!')