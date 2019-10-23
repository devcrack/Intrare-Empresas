# Generated by Django 2.2.3 on 2019-10-21 14:55

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('Empresas', '0001_initial'),
        ('Bitacoras', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='bitacoraempresarial',
            name='id_empleado',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Empresas.Empleado'),
        ),
        migrations.AddField(
            model_name='bitacoraempresarial',
            name='id_emprea',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Empresas.Empresa'),
        ),
        migrations.AddField(
            model_name='bitacoraempresarial',
            name='id_vigilante',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Empresas.Vigilante'),
        ),
        migrations.AddField(
            model_name='bitacora',
            name='id_area',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Empresas.Area'),
        ),
        migrations.AddField(
            model_name='bitacora',
            name='id_caseta',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Empresas.Caseta'),
        ),
        migrations.AddField(
            model_name='bitacora',
            name='id_empleado',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Empresas.Empleado'),
        ),
        migrations.AddField(
            model_name='bitacora',
            name='id_empresa',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Empresas.Empresa'),
        ),
        migrations.AddField(
            model_name='bitacora',
            name='id_vigilante',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Empresas.Vigilante'),
        ),
    ]
