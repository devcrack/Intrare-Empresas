import sys
import populate_scripts.poblar_empresas as populate_companies
import populate_scripts.fill_table_user as populate_user

# def create_users():
#     populate_user.fill_table_user()

def add_users(how_many):
    print('Adding users....\n')
    populate_user.fill_table_user(how_many)


def add_companies(how_many):
    print('Adding companies....\n')
    populate_companies.add_Empresas(how_many)


def main():
    jobs = {
        'add_company':add_companies,
        'add_users':add_users
    }
    option = sys.argv[1]
    hw_many = sys.argv[2]
    print(sys.argv)
    jobs[option](int(hw_many))

if __name__ == '__main__':
    main()