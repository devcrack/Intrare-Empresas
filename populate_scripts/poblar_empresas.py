import os
import django
import random
from faker import Faker
from Empresas.models import *
from Usuarios.models import CustomUser

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ControlAccs.settings')
django.setup()

faker = Faker()
#empresas = ['Draixmailler', 'BMW', 'Cummins', 'DaeLabs', 'General Electric']

def add_Empresas(N=5):
    a_length = len(CustomUser.objects.all())
    for entry in range(N):
        a_user = CustomUser.objects.all()[random.randint(1, a_length - 1)]
        fake_user = a_user
        print(fake_user)
        fake_empresa = faker.company()
        fake_address = faker.street_address()
        fake_numer_phone = faker.msisdn()
        fake_mail = faker.email()
        fake_logo = faker.company_suffix()
        fake_web_page = faker.domain_name()
        fake_scian = random.randint(1,30)
        fake_classification = faker.job()
        fake_latitude = faker.latitude()
        fake_longitude = faker.longitude()
        fake_url_map = faker.uri()
        fake_validity = faker.date(end_datetime=None)
        fake_empresa = Empresa.objects.get_or_create(
            custom_user=fake_user,
            name=fake_empresa,
            address=fake_address,
            telephone=fake_numer_phone,
            email=fake_mail,
            logo=fake_logo,
            web_page=fake_web_page,
            scian = fake_scian,
            classification=fake_classification,
            latitude=fake_latitude,
            longitude=fake_longitude,
            url_map=fake_url_map,
            validity=fake_validity
        )[0]
        fake_empresa.save()

