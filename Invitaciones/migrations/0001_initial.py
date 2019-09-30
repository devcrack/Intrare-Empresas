# Generated by Django 2.2.3 on 2019-09-30 02:53

import datetime
from django.db import migrations, models
import django.db.models.deletion
from django.utils.timezone import utc


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('Empresas', '0001_initial'),
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
                ('fecha_hora_envio', models.DateTimeField(default=datetime.datetime(2019, 9, 30, 2, 53, 18, 464251, tzinfo=utc))),
                ('typeInv', models.IntegerField(default=0)),
                ('dateInv', models.DateField(default=datetime.datetime(2019, 10, 1, 2, 53, 18, 464251, tzinfo=utc))),
                ('timeInv', models.TimeField(default=datetime.time(0, 0))),
                ('expiration', models.DateField(default=datetime.datetime(2019, 10, 3, 2, 53, 18, 464251, tzinfo=utc))),
                ('diary', models.CharField(default='', max_length=7)),
                ('asunto', models.CharField(max_length=254)),
                ('automovil', models.BooleanField()),
                ('notas', models.CharField(blank=True, default='', max_length=256, null=True)),
                ('empresa', models.CharField(blank=True, default='', max_length=254, null=True)),
                ('leida', models.BooleanField(default=False)),
                ('qr_code', models.CharField(blank=True, max_length=16, unique=True)),
                ('id_admin', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='Empresas.Administrador')),
                ('id_area', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Empresas.Area')),
                ('id_empleado', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='Empresas.Empleado')),
                ('id_empresa', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='id_company_inv', to='Empresas.Empresa')),
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
                ('idInvitacion', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Invitaciones.Invitacion')),
            ],
            options={
                'verbose_name_plural': 'InvitacionesReferido',
            },
        ),
    ]
