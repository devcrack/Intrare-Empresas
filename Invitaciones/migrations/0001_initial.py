# Generated by Django 2.2.3 on 2019-10-14 15:33

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
                ('id_empresa', models.IntegerField()),
                ('id_area', models.IntegerField()),
                ('dateInv', models.DateField(default=datetime.datetime(2019, 10, 14, 0, 0))),
                ('timeInv', models.TimeField()),
                ('diary', models.CharField(default='', max_length=7)),
                ('asunto', models.CharField(max_length=254)),
                ('automovil', models.BooleanField()),
                ('notas', models.CharField(blank=True, default='', max_length=256, null=True)),
                ('empresa', models.CharField(blank=True, default='', max_length=254, null=True)),
                ('leida', models.BooleanField(default=False)),
                ('dateSend', models.DateTimeField(default=datetime.datetime.now)),
                ('referredMail', models.EmailField(default=None, max_length=254, null=True)),
                ('referredPhone', models.CharField(default=None, max_length=12, null=True)),
                ('qrCode', models.CharField(blank=True, max_length=14, unique=True)),
                ('maxForwarding', models.IntegerField(default=3)),
            ],
            options={
                'verbose_name_plural': 'InvitacionesReferido',
            },
        ),
    ]
