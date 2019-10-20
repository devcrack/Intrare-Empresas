# Generated by Django 2.2.3 on 2019-10-20 21:41

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Acceso',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fecha_hora_acceso', models.DateTimeField(default=datetime.datetime.now)),
                ('fecha_hora_salida', models.DateTimeField(blank=True, default=None, null=True)),
                ('estado', models.IntegerField(default=1)),
                ('pase_salida', models.BooleanField(blank=True, default=False)),
                ('motivo_no_firma', models.TextField(blank=True, max_length=400, null=True)),
                ('comentarios_VE', models.TextField(blank=True, max_length=300, null=True)),
                ('datos_coche', models.TextField(blank=True, null=True)),
                ('equipo', models.TextField(blank=True, default=None, null=True)),
                ('qr_code', models.CharField(max_length=30, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Administrador',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
            options={
                'verbose_name_plural': 'Administradores',
            },
        ),
        migrations.CreateModel(
            name='Area',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=100)),
                ('color', models.CharField(max_length=7)),
            ],
        ),
        migrations.CreateModel(
            name='Caseta',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=100)),
                ('activa', models.BooleanField()),
            ],
        ),
        migrations.CreateModel(
            name='Empleado',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('extension', models.CharField(max_length=10)),
                ('puede_enviar', models.BooleanField()),
                ('id_notificaciones', models.CharField(max_length=100)),
                ('codigo', models.CharField(max_length=20)),
            ],
            options={
                'verbose_name_plural': 'Empleados',
            },
        ),
        migrations.CreateModel(
            name='Empresa',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, unique=True)),
                ('address', models.CharField(max_length=200)),
                ('telephone', models.CharField(blank=True, max_length=30, unique=True)),
                ('email', models.EmailField(max_length=100, unique=True)),
                ('logo', models.ImageField(default=None, max_length=256, upload_to='Logos')),
                ('web_page', models.CharField(max_length=100)),
                ('scian', models.IntegerField()),
                ('classification', models.CharField(max_length=100)),
                ('latitude', models.FloatField()),
                ('longitude', models.FloatField()),
                ('url_map', models.CharField(max_length=200)),
                ('validity', models.DateField()),
            ],
        ),
        migrations.CreateModel(
            name='SecurityEquipment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nameEquipment', models.CharField(max_length=254)),
            ],
            options={
                'verbose_name_plural': 'Equipment Security',
            },
        ),
        migrations.CreateModel(
            name='Veto',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fecha_hora_veto', models.DateTimeField(auto_now_add=True)),
                ('motivo', models.TextField()),
                ('tipo', models.CharField(max_length=45)),
            ],
        ),
        migrations.CreateModel(
            name='Vigilante',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('id_empresa', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Empresas.Empresa')),
            ],
            options={
                'verbose_name_plural': 'Vigilantes',
            },
        ),
    ]
