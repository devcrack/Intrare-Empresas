import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ControlAccs.settings')
import django
django.setup()

from Empresas.models import Area, Empresa
from faker import Faker

#Posibles Áreas de una  Empresa
AREAS = [
    'Gerencia',
    'Recursos Humanos',
    'Administración',
    'Sistemas',
    'Compras',
    'Producción',
    'Marketing',
    'Finanzas',
    'Matenimiento',
    'Laboratorio'
]

obj = Faker()


def fill_area_table(N=5):
    num_empresas = len(Empresa.objects.all())
    if num_empresas > 1:
        for i in range(num_empresas - 1):
            a_company = Empresa.objects.all()[i]
            for j in range(0, 5):
                nombre = AREAS[j]
                color = obj.hex_color()
                area = Area.objects.get_or_create(
                    id_empresa=a_company,
                    nombre=nombre,
                    color=color
                )[0]
                area.save()
    else:
        print('You must to add some Companies first\n')

# if __name__ == '__main__':
#     print('Filling random data')
#     fill_table_area()
#     print('Filling Done!!!')