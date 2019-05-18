
from django.core.exceptions import ObjectDoesNotExist
from . import *
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


def add_companies(n=1):
    """
    :param n:
    :return:
    Todo:
        * Generar un Administrador del sistema para cada Compañia/Empresa.
    """
    num_parques = len(Parque.objects.all())
    if num_parques > 0:
        parque = Parque.objects.all()[random.randint(1, num_parques - 1)]
    else:
        parque = None
        for entry in range(n):
            sys_admin = add_user(False, settings.ADMIN)
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
            for i in range(count_companies):
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


def add_areas(n=1):
    _companies = Empresa.objects.all()
    count_companies = len(_companies)
    if count_companies > 0:
        for i in range(0, count_companies):
            # a_company = Empresa.objects.all()[i]
            _company = _companies[i]
            _company = Empresa(_company)
            for j in range(0, n):
                name = AREAS[j]
                _color = str(faker.hex_color())
                area = Area.objects.get_or_create(
                    id_empresa=_company.id,
                    nombre=name,
                    color=_color
                )[0]
                area.save()
                print('Company ID#' + str(_company.id) + 'Area #' + str(j) + ' ADDED\n')
    else:
        print('You must to add some Companies first\n')


def add_casetas(N=5):
    count_companies = len(Empresa.objects.all())
    if count_companies > 0:
        for i in range(count_companies):
            a_company = Empresa.objects.all()[i]
            for j in range(N):
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


def add_employees_random_area(n):
    """Add a set of employees to employees table of App Company.
    Here we add a certain number of employees to all companies but to a random Area of
    each company.
    Args:
        n(int): Number of employees that you want add to data base table.
    Todo:
        *
    """
    num_companies = len(Empresa.objects.all())
    if num_companies > 0 :
        for i in range(0, num_companies):
            # Seleccionamos la empresa para agregar el empleado
            _empresa = Empresa.objects.all()[i]
            try:
                # Get all areas of current company
                _areas = Area.objects.filter(id_empresa=_empresa.id)
                num_areas = len(_areas)
                _area = _areas[random.randint(0, num_areas - 1)]
                _id_area = _area.id
            except ObjectDoesNotExist:
                print('You must to add some Areas first to this ID' + str(_empresa.id) + '\n')
            for j in range(n):
                _id_usuario = add_user(False, settings.EMPLEADO)
                _extension = phn()
                _puede_enviar = bool(random.getrandbits(1))
                _id_notifiaciones = phn()
                _codigo = phn()
                _empleado = Empleado.objects.get_or_create(
                    id_empresa=_empresa,
                    id_usuario=_id_usuario,
                    id_area=_area,
                    extension=_extension,
                    puede_enviar=_puede_enviar,
                    id_notificaciones=_id_notifiaciones,
                    codigo=_codigo
                )[0]
                _empleado.save()


def add_employee_all_areas(n=1):
    """Add a certain number of employees to all companies and its areas ech one
    of it, in other words to all areas of each company.

    :return VOID:
    """
    _companies = Empresa.objects.all()
    num_companies = len(_companies)
    if num_companies > 0:
        for index_company in range(0, num_companies):
            # Get the current company
            _company = _companies[index_company]
            _company = Empresa(_company)
            # Get all areas
            _areas = Area.objects.filter(id_empresa=_company.id)
            _num_areas = len(_areas)
            if _num_areas:
                for index_area in range(0, _num_areas):
                    _area = _areas[index_area]
                    _area = Area(_area)
                    for num_employee in range(0, n):
                        _user = add_user(False, settings.EMPLEADO)
                        _extension = phn()
                        _can_sent = True
                        _id_notify = phn()
                        _code =  phn()
                        _employee = Empleado.objects.get_or_create(
                            id_empresa=_company.id, id_usuario=_user,
                            id_area=_area.id, extension=_extension,
                            puede_enviar=_can_sent, id_notificaciones=_id_notify,
                            codigo=_code
                        )[0]
                        _employee.save()
                        print('Company ID#' + str(_company.id) +  ';Area ID#' +
                              str(_area.id) + 'Employee #' + str(num_employee + 1) + ' CREATED\n')
            else:
                print('Add some areas to this company with this ID=' + str(_company.id) + ' first \n')
    else:
        print('Add some companies first \n')


def add_guard(N=1):
    """Add a guard

    Args:
        N(int):Por default son 10 registro pero en realidad puede tomar el valor que le sea proporcionado.

    Todo:
        * Primero que nada se tiene que dar de alta un usuario.
        * Al dar de alta un usario como vigilante hay que tener especial cuidado de los campos
          que vamos a dar de alta para dicho registro.
        * Una vez que se haya creado el usuario hay que vincularlo con el vigilante.

    """
    num_companies = len(Empresa.objects.all())
    if num_companies:
        for i in range(0, num_companies):
            _company = Empresa.objects.all()[i]
            for j in range(N):
                _user = add_user(False,settings.VIGILANTE)
                _new_guard = Vigilante.objects.get_or_create(id_empresa=_company, id_usuario=_user)
    else:
        print('Add some companies first of all\n')
        return 0

