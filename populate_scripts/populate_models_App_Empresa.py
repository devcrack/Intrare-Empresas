import os
import django
import random
from django.core.exceptions import ObjectDoesNotExist

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ControlAccs.settings')
django.setup()

from Empresas.models import  *
from Usuarios.models import CustomUser
from Invitaciones.models import Invitacion
from faker import Faker
from .random_number_phone import phn
from Parques.models import Parque

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

#Posibles Nombres de Casetas
CASETAS = [
    'Norte',
    'Sur',
    'Este',
    'Oeste'
]


faker = Faker()

def add_vigilante():
    """Se agrega un determinado numero de registros a la tabla Vigilante.

    Args:
        N(int):Por default son 10 registro pero en realidad puede tomar el valor que le sea proporcionado.


    Todo:
        * Primero que nada se tiene que dar de alta un usuario.
        * Al dar de alta un usario como vigilante hay que tener especial cuidado de los campos
          que vamos a dar de alta para dicho registro.
        * Una vez que se haya creado el usuario hay que vincularlo con el vigilante.
        * Los vigilantes siempre se consideran como agentes externos a la empresa(Empresa de seguridad) ??,
          o en caso de ser vigilantes de la empresa, PASAN A ser EMPLEADOS????.
    """
    a_length = len(Empresa.objects.all())
    if a_length > 0:
        # Obtenemos un registro de la tabla empresa para vincularla con el vigilante  a generar.
        _empresa = Empresa.objects.all()[random.randint(1, a_length - 1)]
        _id_empresa = _empresa.id
        #Generemos un usuario que sera el vigilante, NO ES SUPER USARIO
        _user = add_user(False)
        #Se tiene que cargar que el perfil del usuario recien creado es un empleado.
        #ERROR_perfil = Perfil.objects.get_or_create(id=_user.user_perfil.id)
        #ERROR_perfil.es_empleado = True
        #Se tiene que cargar el numero telefonico del Guardia en Perfil.
        #ERROR_perfil.celular = faker().msisdn()
        #ERROR_perfil.save()
        # Generar el nuevo Vigilante
        _vigilante = Vigilante.objects.get_or_create(id_empresa=_empresa, id_usuario=_user)[0]
        _vigilante.save()
        return _vigilante
    else:
        print('Agrega registro a la tabla empresas\nNANI\n')
        return 0


def add_user(_is_superuser):
    full_name = faker.name()
    list = full_name.split()
    name = list[0] # Requiere: Vigalante,
    last_name = list[1] # Requiere: Vigiliante
    email = faker.email()
    username_pre = email.split("@")
    username = username_pre[0]
    password = faker.password()
    is_staff = False
    is_active = True
    is_superuser = _is_superuser
    last_login = faker.date_time()
    user = CustomUser.objects.get_or_create(
        first_name=name,
        last_name=last_name,
        username=username,
        email=email,
        is_staff=is_staff,
        is_active=is_active,
        is_superuser=is_superuser,
        last_login=last_login,
        password=password)[0]
    user.save()

    return user


def add_acceso():
    """
    Aqui al seleccionar la empresa puede ser random,
    el area debera estar vinculado a esta empresa pero tambien puede ser random,
    el empleado tendra que estar vinculado a esta empresa pero tambien puede ser random.
    El usuario se toma de la invitacion, para esto se tiene que hacer la interseccion
    con la empresa, el area y el empleado.

    Obtener una invitacion random y concederle acceso
    :return:
    Todo:
        * La seleccion de la empresa es random.
        * Area vinculada a la empresa seleccionada.
        * Empleado vinculado a la empresa.
        * Obtener la invitacion relacionada a esta area.
    """
    #Obtenemos la empresa en la que se concedera el acceso.
    num_inv = len(Invitacion.objects.all())
    if num_inv > 1:
        _invitacion = Invitacion.objects.all()[random.randint(1, num_inv - 1)]
        #Empresa donde se la esta dando acceso
        _id_empresa = _invitacion.id_empresa
        #Area de la empresa donde se esta dando el acceso.
        _id_area  = _invitacion.id_area
        #¿¿¿Empleado que esta dando el Acceso??, o ¿Que genero al invitacion?
        employee_or_guard = bool(random.getrandbits(1))
        #Eligimos quien da el acceso a esta invitacion.
        if employee_or_guard: #El acceso se lo concedera un empleado,
            #Si el acceso se lo concedio un empleado entonces tenenmos que obtener el
            #Identificador del Empleado.
            #_empleado_acceso =
            pass
        else : #El acceso se lo concedera un guardia
            _id_empleado = _invitacion.id_empleado


    else:
        print("Add some invitations first of all, please \n")






    num_company = len (Empresa.objects.all())
    if num_company > 0:
        # Obtenemos un registro de la tabla empresa para vincularla con el vigilante  a generar.
        _empresa = Empresa.objects.all()[random.randint(1, num_company - 1)]
        _id_empresa = _empresa.id

        # Obtenemos el area de la empresa con la que actualmente se esta trabajando, para generar la invitacion.
        try:
            _area_empresa = Area.objects.get(id=_id_empresa)
        except ObjectDoesNotExist:
            print("Agrega Areas vinculadas a la empresa con este Id" + str(_id_empresa) + "\n")
            return 0
        # Obtenemos el empleado que pertenece a esta empresa, es decir quien concedio el acceso
        try:
            _empleado = Empleado.objects.get(_id_empresa)
        except ObjectDoesNotExist:
            print("Agrega Areas empleados a la empresa con este Id" + str(_id_empresa) + "\n")
            return 0


    else:
        print("Add some companies first of all, please \n")

def add_companies(N=5):
    """

    :param N:
    :return:
    Todo:
        * Generar un Administrador del sistema para cada Compañia/Empresa.
    """
    num_parques = len(Parque.objects.all())
    if num_parques > 0:
        parque = Parque.objects.all()[random.randint(1, num_parques - 1)]
    else:
        parque = None
        for entry in range(N):
            sys_admin = add_user(True, 0)
            fake_empresa = faker.company()
            fake_address = faker.street_address()
            fake_numer_phone = phn()
            fake_mail = faker.email()
            fake_logo = faker.company_suffix()
            fake_web_page = faker.domain_name()
            fake_scian = random.randint(1, 30)
            fake_classification = faker.job()
            fake_latitude = faker.latitude()
            fake_longitude = faker.longitude()
            fake_url_map = faker.uri()
            fake_validity = faker.date_time()
            fake_empresa = Empresa.objects.get_or_create(
                custom_user=sys_admin,
                id_parque=parque,
                name=fake_empresa,
                address=fake_address,
                telephone=fake_numer_phone,
                email=fake_mail,
                logo=fake_logo,
                web_page=fake_web_page,
                scian=fake_scian,
                classification=fake_classification,
                latitude=fake_latitude,
                longitude=fake_longitude,
                url_map=fake_url_map,
                validity=fake_validity
            )[0]
            fake_empresa.save()
        else:
            print("Agrega uno o mas parques \n")



def add_managers(N=5):
    count_users = len(CustomUser.objects.all())
    count_companies = len(Empresa.objects.all())
    count = 0
    if count_users > 1:
        if count_companies > 0:
            for i in range(0, count_companies):
                a_company = Empresa.objects.all()[i]
                a_user = CustomUser.objects.get(id=a_company.custom_user.id)
                print(a_user)
                manager = Administrador.objects.get_or_create(
                    id_empresa=a_company,
                    id_usuario=a_user
                )[0]
                count += 1
        else:
            print('You must to add Companies first!!!\n')
    else:
        print('You must to add some Users first!!!\n')

    print(str(count) + " Managers Added")

def add_areas(N=5):
    count_companies = len(Empresa.objects.all())
    if count_companies > 0:
        for i in range(0, count_companies):
            a_company = Empresa.objects.all()[i]
            for j in range(N):
                nombre = AREAS[j]
                color = faker.hex_color()
                area = Area.objects.get_or_create(
                    id_empresa=a_company,
                    nombre=nombre,
                    color=color
                )[0]
                area.save()
    else:
        print('You must to add some Companies first\n')

def add_casetas(N=5):
    count_companies = len(Empresa.objects.all())
    if count_companies > 1:
        for i in range(count_companies):
            a_company = Empresa.objects.all()[i]
            for j in range(0, 3):
                nombre = CASETAS[j]
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

def add_employees(N=5):
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
                                                extension=faker.msisdn(),
                                                puede_enviar=puede_enviar,
                                                id_notificaciones=faker.msisdn(),
                                                codigo=faker.msisdn()
                                            )[0]
                                    employee.save()
                                    count = count + 1
                                    #perfil = Perfil.objects.get(id=a_user.user_perfil.id)
                                    #perfil.es_empleado = True
                                    #perfil.save()
                else:
                    print('You must to add some Areas first!!!')
            else:
                print("You must to add some campanies first!!!")
        else:
            print("You must to add some Users first!!!")
    print(str(count) + ' employees were added!!!')



def add_user(_is_superuser, type_rol):
    """Crea un usuario.

    Args:
        _is_superuser : Bandera que determina si es un super usuario, Solamente el STAFF es super Usuario.
                        Tipos de Rol:
                            0: Usuario de App,
                            1 Staff,
                            2: Administrador de Sistema,
                            3: Vigilante Parque,
                            4: Administrador Parque,


        type_rol: Tipo de rol que tiene el usuario.
    """
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
    is_superuser = _is_superuser
    _celular = phn()
    _rol = type_rol
    last_login = faker.date_time()
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
        celular=_celular,
        roll=_rol
        )[0]
    user.save()
    print('si sale??????????')
    return user
