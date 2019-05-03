import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ControlAccs.settings')
import django
django.setup()

from Usuarios.models import CustomUser
from faker import Faker

from random import randint, uniform,random


obj = Faker()

def fill_table_user(N=10):
    for i in range(N):
        full_name = obj.name()
        list = full_name.split()
        name = list[0]
        last_name = list[1]
        email = obj.email()
        username_pre = email.split("@")
        username = username_pre[0]
        password = obj.password()
        num_random = randint(0,1)
        if num_random == 0:
            is_staff = False
        else:
            is_staff = True
        if num_random == 0:
            is_active = False
        else:
            is_active = True
        if num_random == 0:
            is_superuser = False
        else:
            is_superuser = True
        last_login = obj.date_time()
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
        return user

if __name__ == '__main__':
    print('Filling random data')
    fill_table_user()
    print('Filling Done!!!')