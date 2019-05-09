import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ControlAccs.settings')
import django
django.setup()

from Empresas.models import  Empresa, Empleado, Area
from Usuarios.models import CustomUser, Perfil
from faker import Faker

import random

obj = Faker()


def fill_employee_table(N=5):
    count = 0
    for i in range(N):
        num_usuarios = len(CustomUser.objects.all())
        #Verificamos que no solamente haya sido dado de alta el Superusuario
        if num_usuarios > 1:
            num_empresas = len(Empresa.objects.all())
            if num_empresas > 1:
                a_company = Empresa.objects.all()[random.randint(1, num_empresas - 1)]
                if len(Area.objects.all().filter(id_empresa=a_company.id)):
                    area_empresa = Area.objects.all().filter(id_empresa=a_company.id)[random.randint(1, 4)]
                    print('AREA')
                    print(area_empresa)
                    a_user = CustomUser.objects.all()[random.randint(1, num_usuarios - 1)]
                    if a_user.is_active:
                        if not a_user.is_staff:
                            if not a_user.is_superuser:
                                if not a_user.user_perfil.es_empleado:
                                    num = random.randint(0, 1)
                                    if num == 0:
                                        puede_enviar = False
                                    else:
                                        puede_enviar = True
                                    employee = Empleado.objects.get_or_create(
                                                id_empresa=a_company,
                                                id_usuario=a_user,
                                                id_area=area_empresa,
                                                extension=obj.msisdn(),
                                                puede_enviar=puede_enviar,
                                                id_notificaciones=obj.msisdn(),
                                                codigo=obj.msisdn()
                                            )[0]
                                    employee.save()
                                    count = count + 1
                                    perfil = Perfil.objects.get(id=a_user.user_perfil.id)
                                    perfil.es_empleado = True
                                    perfil.save()
                else:
                    print('You must to add some Areas first!!!')
            else:
                print("You must to add some campanies first!!!")
        else:
            print("You must to add some Users first!!!")
    print(str(count) + ' were added employees!!!')