"""Script para generar registros Fake de manera automatica.

"""


import sys
from builtins import print

import populate_scripts.poblar_empresas as populate_companies
import populate_scripts.fill_table_user as populate_user
import populate_scripts.fill_area_table as populate_area
import populate_scripts.fill_caseta_table as populate_caseta
import populate_scripts.fill_employee_table as populate_employee
import populate_scripts.fill_manager_table as populate_manager

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
    populate_companies.add_Empresas(how_many)



def add_area(how_many):
    print('Adding areas....\n')
    populate_area.fill_area_table(how_many)

def add_caseta(how_many):
    print('Adding casetas....\n')
    populate_caseta.fill_caseta_table(how_many)

def add_employees(how_mamy):
    print('Add employees...\n')
    populate_employee.fill_employee_table(how_mamy)

def add_managers(how_many):
    print('Adding mangers')
    populate_manager.fill_manager_table(how_many)


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
        'add_casetas':add_caseta,
        'add_employees':add_employees,
        'add_managers':add_managers
    }
    option = sys.argv[1]
    hw_many = sys.argv[2]
    print(sys.argv)
    jobs[option](int(hw_many))

if __name__ == '__main__':
    main()