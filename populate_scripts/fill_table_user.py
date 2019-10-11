import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ControlAccs.settings')
django.setup()

from Usuarios.models import CustomUser
from faker import Faker
import random
import pytz

obj = Faker()


def fill_table_user(N=5):
    for i in range(N):
        full_name = obj.name()
        list = full_name.split()
        name = list[0]
        last_name = list[1]
        email = obj.email()
        username_pre = email.split("@")
        username = username_pre[0]
        password = obj.password()
        is_staff = False
        is_active = True
        is_superuser = False
        last_login = obj.date_time_between(
            start_date="+3d", 
            end_date="+30d", 
            tzinfo=pytz.timezone('America/Mexico_City'))
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
        user.save()


if __name__ == '__main__':
    print('Filling random data')
    fill_table_user()
    print('Filling Done!!!')