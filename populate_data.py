import populate_scripts.fill_table_user as populate_user
import populate_scripts.poblar_empresas as populate_companies
from Usuarios.models import CustomUser

# def create_users():
#     populate_user.fill_table_user()

def agregar_empresas():
    user = populate_user.fill_table_user()
    a_user = CustomUser.objects.first()
    populate_companies.add_Empresas(15, a_user)


if __name__ == '__main__':
    agregar_empresas()