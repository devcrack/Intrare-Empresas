# Generated by Django 2.2.3 on 2019-10-30 18:50

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Empresas', '0002_auto_20191021_0955'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='empleado',
            name='codigo',
        ),
        migrations.RemoveField(
            model_name='empleado',
            name='id_notificaciones',
        ),
    ]
