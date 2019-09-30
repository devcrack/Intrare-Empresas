# Generated by Django 2.2.3 on 2019-09-30 20:11

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='EquipoSeguridad',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=254, unique=True)),
            ],
            options={
                'verbose_name_plural': 'EquipoSeguridad',
            },
        ),
        migrations.CreateModel(
            name='EquiposporInvitacion',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
            options={
                'verbose_name_plural': 'Security Equipment by Invitation',
            },
        ),
        migrations.CreateModel(
            name='Invitacion',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fecha_hora_envio', models.DateTimeField(default=datetime.datetime.now)),
                ('typeInv', models.IntegerField(default=0)),
                ('dateInv', models.DateField()),
                ('timeInv', models.TimeField()),
                ('expiration', models.DateField()),
                ('diary', models.CharField(default='', max_length=7)),
                ('asunto', models.CharField(max_length=254)),
                ('automovil', models.BooleanField()),
                ('notas', models.CharField(blank=True, default='', max_length=256, null=True)),
                ('empresa', models.CharField(blank=True, default='', max_length=254, null=True)),
                ('leida', models.BooleanField(default=False)),
                ('qr_code', models.CharField(blank=True, max_length=16, unique=True)),
            ],
            options={
                'verbose_name_plural': 'INVITACIONES',
            },
        ),
        migrations.CreateModel(
            name='InvitacionReferido',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('emailTercero', models.EmailField(max_length=254)),
                ('asignada', models.BooleanField(default=False)),
                ('hashCode', models.CharField(max_length=100, unique=True)),
            ],
            options={
                'verbose_name_plural': 'InvitacionesReferido',
            },
        ),
        migrations.CreateModel(
            name='InvitationByUsers',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
            options={
                'verbose_name_plural': 'UsersByInvitation',
            },
        ),
    ]
