import os
import django
import random
from faker import Faker
from Empresas.models import *

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ControlAccs.settings')
django.setup()

faker = Faker()
#empresas = ['Draixmailler', 'BMW', 'Cummins', 'DaeLabs', 'General Electric']

def add_Empresas(N=10, a_user):
    for entry in range(N):
        fake_user = a_user
        fake_empresa = random.company()
        fake_address = faker.street_address()
        fake_numer_phone = faker.phone_number()
        fake_mail = faker.email()
        fake_logo = faker.company_suffix()
        fake_web_page = faker.domain_name()
        scian = random.randint(1,30)
        fake_classification = faker.job()
        fake_latitude = faker.latitude()
        fake_longitude = faker.longitude()
        fake_url_map = faker.uri()
        fake_validity = faker.date()
        fake_empresa = Empresa.objects.get_or_create(
            custom_user=fake_user,
        )



from Usuarios.models import CustomUser
from faker import Faker