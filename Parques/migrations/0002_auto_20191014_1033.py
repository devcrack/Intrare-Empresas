# Generated by Django 2.2.3 on 2019-10-14 15:33

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('Empresas', '0002_auto_20191014_1033'),
        ('Parques', '0001_initial'),
        ('Invitaciones', '0002_auto_20191014_1033'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='vigilanteparque',
            name='id_usuario',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='administradorparque',
            name='id_parque',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Parques.Parque'),
        ),
        migrations.AddField(
            model_name='administradorparque',
            name='id_usuario',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='accesoparque',
            name='id_empresa',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Empresas.Empresa'),
        ),
        migrations.AddField(
            model_name='accesoparque',
            name='id_invitacion',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Invitaciones.Invitacion'),
        ),
        migrations.AddField(
            model_name='accesoparque',
            name='id_parque',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Parques.Parque'),
        ),
        migrations.AddField(
            model_name='accesoparque',
            name='id_usuario',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='accesoparque',
            name='id_vigilante_parqueEnt',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='p_entrada', to='Empresas.Vigilante'),
        ),
        migrations.AddField(
            model_name='accesoparque',
            name='id_vigilante_parqueSal',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='p_salida', to='Empresas.Vigilante'),
        ),
    ]
