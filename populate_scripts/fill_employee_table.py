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
                try:
                    a_company = Empresa.objects.all()[random.randint(1, num_empresas - 1)]
                    print('EMPRESAAA')
                    print(a_company)
                    area_empresa = Area.objects.all().filter(id_empresa=a_company.id)[random.randint(1, 5)]
                    print('AREASSSS')
                    print(area_empresa)
                    # print(areas_empresa)
                    if area_empresa:
                        a_user = CustomUser.objects.all()[random.randint(1, num_usuarios - 1)]
                        print('USUARIO')
                        print(a_user)
                        print(a_user.id)
                        print(a_user.is_active)
                        print(a_user.is_staff)
                        print(a_user.is_superuser)
                        print(a_user.user_perfil.es_empleado)
                        if a_user.is_active and not a_user.is_staff and not a_user.is_superuser and not a_user.user_perfil.es_empleado:
                            num = random.randint(0, 1)
                            if num == 0:
                                puede_enviar = False
                            else:
                                puede_enviar = True
                            employee = Empleado.objects.get_or_create(
                                        id_empresa=a_company,
                                        id_usuario=a_user,
                                        id_area=area_empresa,
                                        extension=646436,
                                        puede_enviar= puede_enviar,
                                        id_notificaciones=324234,
                                        codigo=423432

                                    )[0]
                            employee.save()
                            count = count + 1
                            perfil = Perfil.objects.get(id=a_user.user_perfil.id)
                            perfil.es_empleado = True
                            perfil.save()
                        else:
                            print('Usuario sin permisos')
                    else:
                        print('Aún no hay Áreas dadas de alta en la Empresa')
                except:
                    print("Error")
            else:
                print("You must to add some campanies first!!!")
        else:
            print("You must to add some Users first!!!")
    print('Se Agregaron ' + str(count) + ' Empleados')

# if __name__ == '__main__':
#     print('Filling random data')
#     fill_table_area()
#     print('Filling Done!!!')