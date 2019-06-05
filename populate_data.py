"""Script para generar registros Fake de manera automatica.

"""


import sys
from builtins import print

import populate_scripts.fill_table_user as populate_user
import populate_scripts.populate_models_App_Empresa as populate_company
import populate_scripts.pupulate_models_app_Parques as populate_parks
import populate_scripts.populate_models_app_Grupo as populate_groups
import populate_scripts.populate_models_app_invitaciones as inv
# def create_users():
#     populate_user.fill_table_user()

def add_users(how_many):
    """Agrega registros fake para la tabla Usuarios de la aplicacion Empresa.


    Args:
        how_many(int): Numero de registro que desea agregar a la base de datos.

    """
    print('Adding users....\n')
    for entry in range(how_many):
        populate_company.add_user(False, 2)


def add_companies(how_many):
    """Agrega registros fake para la tabla Empresa de la aplicacion Empresa.

    Args:
        how_many(int): Numero de registro que desea agregar a la base de datos.
    """
    print('Adding companies....\n')
    if len(sys.argv) > 4:
        print("Password")
        print(sys.argv[4])
        populate_company.add_companies(how_many, sys.argv[3], sys.argv[4])
    else:
        populate_company.add_companies(how_many)

def add_invitations(how_many):
    """Agrega un determinado numero de invitaciones
     Args:
         how_many(int):Numero de invitaciones que se desea dar de alta.
    """

    print("Adding Invitation...\n")
    inv.add_invitation(how_many)


def add_tmp_inv(how_many):

    inv.add_temp_invitation(how_many)


def add_security_equp(how_many):
    print('Adding security equipment...\n')
    inv.add_security_equipment(how_many)

def add_area(how_many):
    """
    Agrega áreas a cada Empresa.
    :param how_many: Número de Áreas por Empresa a agregar.
    Nota: how_many no debe ser mayor a 10.
    """
    print('Adding areas....\n')
    populate_company.add_areas(how_many)

def add_casetas(how_many):
    """
    Agrega Casetas a cada Empresa.
    :param how_many: Número de Casetas por Empresa a Agregar.
    Nota: how_many no debe ser mayor a 4.
    """
    print('Adding casetas....\n')
    populate_company.add_casetas(how_many)


def add_employees(how_many):
    print('Add employees...\n')
    if len(sys.argv) > 4:
        print("Password")
        print(sys.argv[4])
        populate_company.add_employee_all_areas(how_many, sys.argv[3], sys.argv[4])
    else:
        populate_company.add_employee_all_areas(how_many)


def add_guards(how_many):
    print('Adding  guards..\n')
    populate_company.add_guard(how_many)

def add_access(how_many):
    print('Adding access')
    populate_company.add_acceso(how_many)

def add_parks(how_many):
    print('Adding parks')
    populate_parks.add_Parques(how_many)


def add_groups(how_many):
    """
    Agrega un determinado número de Grupos.
    :param how_many: Número de registros a agregar.
    """
    print('Adding groups...')
    populate_groups.add_group(how_many)

    
def add_contacts(how_many):
    """
    Agrega un determinado número de Contactos.
    :param how_many: Número de registros a agregar.
    """
    print('Adding contacts...')
    populate_groups.add_contact(how_many)

    
def add_group_has_contacts(how_many):
    """
    Agrega un determinado número de registros a la
    Tabla Group_has_contacts.
    :param how_many: Número de registros a agregar.
    """
    print('Adding contacts per Groups...')
    populate_groups.add_group_has_contact(how_many)



def  add_invitation_from_user(how_many):
    inv.employee_add_invitation(how_many, sys.argv[3])


def main():
    """Entrada principal para llevar a cabo la ejecucion de este script

    Las funciones se llaman mediante un diccionario simple para hacer uso de
    la linea de comandos a un nivel muy simple y basico


    Attributes:
        jobs(dict): Diccionaro que relaciona el argumento con la funcion que tiene que ser ejecutada.
        option(strin):Cadena que se recibio como argumento y que es la clave para nuestro diccionario(jobs)
        hw_many(int): La cantidad de registro que se van a generar.


    Examples:
        Ejecucion del script para generar 200 registros a la tabla Empresa.
        >>python populate_data.py add_company 200
    """


    jobs = {
        'add_company': add_companies, #1
        'add_users': add_users,
        'add_areas': add_area,        #2
        'add_casetas': add_casetas,
        'add_employee': add_employees,
        'add_invitation': add_invitations,
        'add_access': add_access,
        'add_tmp_invitation': add_tmp_inv,
        'add_parques': add_parks,
        'add_guards': add_guards,
        'add_contacts': add_contacts,
        'add_groups': add_groups,
        'add_group_has_contacts': add_group_has_contacts,
        'add_security_equipment': add_security_equp,
        'add_inv': add_invitation_from_user
    }

    option = sys.argv[1]
    if len(sys.argv) == 3:
        hw_many = sys.argv[2]
    else:
        hw_many = 1
    jobs[option](int(hw_many))

    
if __name__ == '__main__':
    main()
