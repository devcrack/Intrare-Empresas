import os
import django
import random

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ControlAccs.settings')
django.setup()

from Empresas.models import Administrador, Empresa
from Usuarios.models import CustomUser

def fill_manager_table(N=5):
    count_users = len(CustomUser.objects.all())
    count_companies = len(Empresa.objects.all())
    count = 0
    if count_users > 1 and count_companies > 0:
        a_company = Empresa.objects.all()[random.randint(0, count_companies - 1)]
        if count_companies > 0:
            for i in range(1, count_users - 1):
                a_user = CustomUser.objects.all()[i]
                if not a_user.is_superuser:
                    if not a_user.is_staff:
                        if not a_user.user_perfil.es_empleado:
                            if a_user.is_active:
                                manager = Administrador.objects.get_or_create(
                                    id_empresa=a_company,
                                    id_usuario=a_user
                                )[0]
                                a_user.is_superuser = True
                                a_user.save()
                                manager.save()
                                count += count
        else:
            print('You must to add Companies first!!!\n')
    else:
        print('You must to add some Userss first!!!\n')

    print(str(count) + " Managers Added")