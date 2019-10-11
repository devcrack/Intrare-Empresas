from faker import Faker
import os
import django
import random
from django.db import models
"""Importamos todos nuestros modelos"""
from aplicacion_name.models import _a_model_name

"""Importar la configuracion de DJANGO"""
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ControlAccs.settings')
django.setup()

"""Modelos Usados en el ejemplo"""
class School(models.Model):
    name = models.CharField(max_length=250, blank=False)
    address = models.CharField(max_length=250, blank=False)
    email = models.EmailField(blank=False)
    phone_number = models.PositiveIntegerField(blank=False, max_length=13)

class Student(models.Model):
    name = models.CharField(max_length=250, blank=False)
    age = models.PositiveIntegerField(blank=False, max_length=3)
    school = models.ForeignKey(School, on_delete=models.CASCADE)


faker = Faker()

schools = ['DPS', 'HARVARD', 'SMS', 'VMPS']

fake_address = faker.address()
fake_mail = faker.email()
fake_number = faker.number()

def add_school():
    fake_school = School.objects.get_or_create(
        name=random.choice(schools), address = fake_address, email=fake_mail,
        phone_number=fake_number)[0]
    fake_school.save()
    return fake_school

def populate(N=5):
    for entry in range(N):
        a_school = add_school()
        fake_name = faker.name()
        fake_age = faker.phone_number()

        a_student = Student.objects.get_or_create(school=a_school, name=fake_name, age=fake_age)


if __name__ == 'main':
    print('Populating data...Please wait')
    populate(20)
    print('Populate Complete')







