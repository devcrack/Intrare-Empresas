"""Script para generar registros Fake de manera automatica.

"""


import sys
from builtins import print

import populate_scripts.fill_table_user as populate_user
import populate_scripts.populate_models_App_Empresa as populate_company
import populate_scripts.populate_models_app_invitaciones as populate_inv

# def create_users():
#     populate_user.fill_table_user()

def add_users(how_many):
    """Agrega registros fake para la tabla Usuarios de la aplicacion Empresa.


    Args:
        how_many(int): Numero de registro que desea agregar a la base de datos.

    """
    print('Adding users....\n')
    populate_user.fill_table_user(how_many)


def add_companies(how_many):
    """Agrega registros fake para la tabla Empresa de la aplicacion Empresa.


    Args:
        how_many(int): Numero de registro que desea agregar a la base de datos.

    """


    print('Adding companies....\n')
    populate_company.add_companies(how_many)

def agrega_invitaciones(how_many):
    """Agrega un determinado numero de invitaciones

     Args:
         how_many(int):Numero de invitaciones que se desea dar de alta.
    """
    print("Agregando Invitaciones")
    populate_inv.add_Invitaciones(how_many)



def add_area(how_many):
    print('Adding areas....\n')
    populate_company.add_areas(how_many)

def add_casetas(how_many):
    print('Adding casetas....\n')
    populate_company.add_casetas(how_many)

def add_employees(how_mamy):
    print('Add employees...\n')
    populate_company.add_employees(how_mamy)

def add_managers(how_many):
    print('Adding mangers')
    populate_company.add_managers(how_many)


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
        'add_company':add_companies,
        'add_users':add_users,
        'add_areas':add_area,
        'add_casetas':add_casetas,
        'add_employees':add_employees,
        'add_managers':add_managers,
        'add_inv': agrega_invitaciones,
    }
    option = sys.argv[1]
    hw_many = sys.argv[2]
    print(sys.argv)
    jobs[option](int(hw_many))

if __name__ == '__main__':
    main()