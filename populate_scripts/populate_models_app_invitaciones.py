from . import *


def add_invitation(n=1):
    """Add a certain number of invitations to all companies and its  areas, generates by each Employee.

    Args:
        n(int):Por default son 10 registro pero en realidad puede tomar un valor que le sea proporcionado.
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
                    # Get the employees related with current company and area
                    _employees = Empleado.objects.filter(id_empresa=_company.id, id_area=_area.id)
                    num_employees = len(_employees)
                    if num_employees:
                        for index_employee in range(0, num_employees):
                            _employee = _employees[index_employee]
                            _employee = Empleado(_employee)
                            for entry in range(n):
                                _user = add_user(False, 0)
                                _business = faker.text(max_nb_chars=250, ext_word_list=None)
                                _watched = False
                                _from_company = faker.company()
                                _notes = faker.text(max_nb_chars=100, ext_word_list=None)
                                _car = bool(random.getrandbits(1))
                                _date_sent = faker.date_time()
                                _date_invitation = faker.date_time()
                                _invitation = Invitacion.objects.get_or_create(
                                    id_empresa=_company.id, id_area=_area.id,
                                    id_empleado=_employee.id, id_usuario=_user,
                                    leida=_watched, empresa=_from_company,
                                    notas=_notes, automovil=_car, asunto=_business,
                                    fecha_hora_invitacion=_date_invitation,
                                    fecha_hora_envio=_date_sent
                                )[0]
                                _invitation.save()
                                print('Invitation #' + str(entry + 1) + 'Created\n')
                                print('COMPANY='+ str(_company.id) + '\n')
                                print('AREA=' + str(_area.id) + '\n')
                                print('EMPLOYEE that sent Invitation=' + str(_employee.id) + '\n')
                    else:
                        print('You need Add Employees to this Company =' +
                              str(_company.id) + 'and to this Area=' + str(_area.id) + '\n')
            else:
                print('Add some areas to this company with this ID=' + str(_company.id) + ' first \n')
    else:
        print('Add some companies first \n')


def add_temp_invitation(n=1):
    """Add Temporal invitations to all companies all areas generates by its employees.
        Args:
            n(int):Por default son 10 registro pero en realidad puede tomar un valor que le sea proporcionado.
        Attributes:

        Todo:
            * Get Company
            * Get Area related to Company
            * Get employee that create the invitation.
            * Fill data required.
        """
    _companies = Empresa.objects.all()
    num_companies = len(_companies)
    if num_companies:
        for index_company in range(0, num_companies):
            _company = _companies[index_company]
            _company = Empresa(_company)
            _areas = Area.objects.filter(id_empresa=_company.id)
            num_areas = len(_areas)
            if num_areas:
                for index_area in range(0, num_areas):
                    _area = _areas[index_area]
                    _area = Area(_area)
                    # Get the employees related with current company and area
                    _employees = Empleado.objects.filter(id_empresa=_company.id, id_area=_area.id)
                    num_employees = len(_employees)
                    if num_employees:
                        for index_employee in range(0, num_employees):
                            _employee = _employees[index_employee]
                            _employee = Empleado(_employee)
                            for entry in range(n):
                                _date_sent = faker.date_between(start_date='now', end_date='+0d')
                                _date_invitation = faker.date_between(start_date='now', end_date='+1m')
                                _business = faker.text(max_nb_chars=250, ext_word_list=None)
                                _car = bool(random.getrandbits(1))
                                _notes = faker.text(max_nb_chars=100, ext_word_list=None)
                                _from_company = faker.company()
                                _nw_inv_temp = InvitacionTemporal.objects.get_or_create(
                                    id_empresa=_company.id, id_area=_area.id,
                                    id_empleado=_employee.id, celular_invitado=phn(),
                                    fecha_hora_envio=_date_sent, fecha_hora_invitacion=_date_invitation,
                                    asunto=_business, automovil=_car, notas= _notes, empresa=_from_company
                                )[0]
                                _nw_inv_temp.save()
                                print('Temporal Invitation #' + str(entry + 1) + 'CREATED  ' +
                                      'COMPANY=' + str(_company.id) + '  ' +
                                      'AREA=' + str(_area.id) + '  ' +
                                      'EMPLOYEE that sent Invitation=' + str(_employee.id) + '\n')
                    else:
                        print('You need Add Employees to this Company =' +
                              str(_company.id) + 'and to this Area=' + str(_area.id) + '\n')
            else:
                print('Add some areas to this company with this ID=' + str(_company.id) + ' first \n')
    else:
        print('Add some companies first \n')



def add_invitacion_Empresarial():
    """Se agrega un registro a la tabla usuarios.

            Args:
                N(int):Por default son 10 registro pero en realidad puede tomar un valor que le sea proporcionado.

            Attributes:

            Todo:
                * Se tiene que obtener la empresa en la que se esta haciendo la invitacion.
                * Obtener el area vinculada con la empresa en la que se esta haciendo la invitacion.
                * Obtener el empleado vinculado con la empresa, es decir quien genera la invitacion.
                * Generamos el usuario al que le esta asiganda la invitacion.
                * Finalmente se genera la invitacion.
            """
    a_length = len(Empresa.objects.all())
    if a_length > 1:
        # Obtenemos un registro de la tabla empresa para vincularla con las invitaciones a generar.
        _empresa = Empresa.objects.all()[random.randi(1, a_length - 1)]
        _id_empresa = _empresa.id
        # Obtenemos el area de la empresa con la que actualmente se esta trabajando, para generar la invitacion.
        try:
            _area_empresa = Area.objects.get(id=_id_empresa)
        except ObjectDoesNotExist:
            print("Agrega Areas vinculadas a la empresa con este Id" + str(_id_empresa) + "\n")
            return 0
        # Obtenemos el empleado que pertenece a esta empresa, es decir quien genero la invitacion
        try:
            _empleado = Empleado.objects.get(_id_empresa)
        except ObjectDoesNotExist:
            print("Agrega Areas empleados a la empresa con este Id" + str(_id_empresa) + "\n")
            return 0
        # Creamos un usuario para vincularlo a esta invitacion temporal
        _user = add_user(False,2)
        _email = faker.email()
        _fecha_hora_envio = faker.date_time()
        _fecha_hora_invitacion = faker.date_time()
        _asunto = faker.paragraph(max_nb_chars=250, ext_word_list=None)
        _automovil = bool(random.getrandbits(1))
        _notas = faker.paragraph(max_nb_chars=150, ext_word_list=None)
        _empresa = faker.company()
        _leida = False
        invitacion_Empresarial = InvitacionEmpresarial.objects.get_or_create(
            id_empresa=_empresa, id_area=_area_empresa,
            id_empleado=_empleado,email=_email, fecha_hora_envio=_fecha_hora_envio,
            fecha_hora_invitacion=_fecha_hora_invitacion, asunto=_asunto,
            automovil=_automovil, notas=_notas, empresa=_empresa, asignada=False,
            cod_seguridad= '"#$"#$"!"#!"#"#$"#$46486548'
        )
    else:
        print('Agrega registro a la tabla empresas\nNANI\n')
        return 0


def add_security_equipment(n):
    for entry in range(n):
        fake_name = faker.job()
        _equipment_security = EquipoSeguridad.objects.get_or_create(nombre=fake_name)[0]
        _equipment_security.save()
        print('Security #' +str(entry + 1) + 'equipment Added\n')



