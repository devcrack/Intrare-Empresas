import os
from faker import Faker
import random
import django
from django.core.exceptions import ObjectDoesNotExist

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ControlAccs.settings')
django.setup()

from Invitaciones.models import *
from Empresas.models import Empresa, Area, Empleado
from Usuarios.models import CustomUser


faker = Faker()

def add_Invitaciones(N=10):
    """Se agrega un determinado numero de registros a la tabla Invitaciones.

    Args:
        N(int):Por default son 10 registro pero en realidad puede tomar un valor que le sea proporcionado.

    Attributes:

    """

    a_length = len(Empresa.objects.all())
    if a_length > 1:
        # Obtenemos un registro de la tabla empresa para vincularla con las invitaciones a generar.
        _empresa = Empresa.objects.all()[random.randint(1, a_length - 1)]

        id_empresa = _empresa.id
        # Obtenemos el area de la empresa con la que actualmente se esta trabajando, para generar la invitacion.
        try:
            _area_empresa = Area.objects.get(id=id_empresa)
        except ObjectDoesNotExist:
            print("Agrega Areas vinculadas a la empresa con este Id" + str(id_empresa) + "\n")
            return 0
        # Obtenemos el empleado que pertenece a esta empresa, es decir quien genero la invitacion
        try:
            _empleado = Empleado.objects.get(id_empresa)
        except ObjectDoesNotExist:
            print("Agrega Areas empleados a la empresa con este Id" + str(id_empresa) + "\n")
            return 0
        length_user_records = len (CustomUser.objects.all())
        if length_user_records > 1:
            for entry in range(N):
                # Obtenemos un usuario random al que le asignaremos una invitacion creada.
                _usuario = CustomUser.objects.all()[random.randint(1, length_user_records)]
                _fecha_hora_envio = faker.date_time()
                _fecha_hora_invitacion = faker.date_time()
                _asunto = faker.paragraph(max_nb_chars=250, ext_word_list=None)
                _automovil = bool(random.getrandbits(1))
                _notas = faker.paragraph(max_nb_chars=150, ext_word_list=None)
                _Empresa = faker.company()
                _leida = bool(random.getrandbits(1))
                invitacion = Invitacion.objects.get_or_create(
                    id_empresa=_empresa, id_area=_area_empresa,
                    id_empleado=_empleado, id_usuario=_usuario,
                    fecha_hora_envio=_fecha_hora_envio,
                    fecha_hora_invitacion=_fecha_hora_invitacion,
                    asunto=_asunto, automovil=_automovil,
                    notas=_notas, empresa=_empresa,
                    leida=_leida
                )
                invitacion.save()

        else:
            print("Agrega usuarios no administradores " + str(id_empresa) + "\n")
            return 0
    else:
        print('Agrega registro a la tabla empresas\nNANI\n')
        return 0

