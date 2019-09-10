import sys

import populate_scripts.populate_models_app_invitaciones as inv


def get_number_inv_employee():
    email = sys.argv[2]
    print('EMAIL=>' + email)
    inv.number_invitations_by_employee(email)


def main():
    jobs = {
        'get_nmb_inv_employee': get_number_inv_employee
    }
    option = sys.argv[1]
    jobs[option]()


if __name__ == '__main__':
    main()
