# Generated by Django 2.2.3 on 2019-10-18 23:42

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='AccesoParque',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fecha_hora_acceso', models.DateTimeField(default=django.utils.timezone.now)),
                ('fecha_hora_Salida', models.DateTimeField(auto_now=True)),
                ('comentarios', models.CharField(max_length=45)),
            ],
            options={
                'verbose_name_plural': 'Accesos al Parque',
            },
        ),
        migrations.CreateModel(
            name='AdministradorParque',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
            options={
                'verbose_name_plural': 'Administradores del Parque',
            },
        ),
        migrations.CreateModel(
            name='Parque',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=150)),
                ('direccion', models.CharField(max_length=150)),
            ],
            options={
                'verbose_name_plural': 'Parques',
            },
        ),
        migrations.CreateModel(
            name='VigilanteParque',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('id_parque', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Parques.Parque')),
            ],
            options={
                'verbose_name_plural': 'Vigilantes del Parque',
            },
        ),
    ]
