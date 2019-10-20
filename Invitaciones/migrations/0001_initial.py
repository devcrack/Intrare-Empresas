# Generated by Django 2.2.3 on 2019-10-19 19:07

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('Empresas', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Invitacion',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fecha_hora_envio', models.DateTimeField(default=datetime.datetime.now)),
                ('typeInv', models.IntegerField(default=0)),
                ('dateInv', models.DateField()),
                ('timeInv', models.TimeField()),
                ('expiration', models.DateField(default=datetime.date(2019, 10, 20))),
                ('diary', models.CharField(default='', max_length=7)),
                ('asunto', models.CharField(max_length=254)),
                ('automovil', models.BooleanField()),
                ('notas', models.CharField(blank=True, default='', max_length=256, null=True)),
                ('empresa', models.CharField(blank=True, default='', max_length=254, null=True)),
                ('leida', models.BooleanField(default=False)),
            ],
            options={
                'verbose_name_plural': 'INVITACIONES',
            },
        ),
        migrations.CreateModel(
            name='InvitationByUsers',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('qr_code', models.CharField(max_length=30)),
            ],
            options={
                'verbose_name_plural': 'UsersByInvitation',
            },
        ),
        migrations.CreateModel(
            name='ReferredInvitation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fecha_hora_envio', models.DateTimeField(default=datetime.datetime.now)),
                ('dateInv', models.DateField()),
                ('timeInv', models.TimeField()),
                ('expiration', models.DateField(default=datetime.date(2019, 10, 20))),
                ('diary', models.CharField(default='', max_length=7)),
                ('subject', models.CharField(max_length=254)),
                ('vehicle', models.BooleanField()),
                ('notes', models.CharField(blank=True, default='', max_length=256, null=True)),
                ('companyFrom', models.CharField(blank=True, default='', max_length=254, null=True)),
                ('Token', models.CharField(default='f994d0309d9d88', max_length=14)),
                ('referredMail', models.EmailField(default=None, max_length=254)),
                ('referredPhone', models.CharField(default=None, max_length=12, null=True)),
                ('areaId', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Empresas.Area')),
            ],
            options={
                'verbose_name_plural': 'EnterpriseInvitation',
            },
        ),
    ]
