# Generated by Django 2.2.3 on 2019-10-20 22:45

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('Parques', '0001_initial'),
        ('Invitaciones', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('Empresas', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='vigilante',
            name='id_usuario',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='veto',
            name='id_empresa',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Empresas.Empresa'),
        ),
        migrations.AddField(
            model_name='veto',
            name='id_usuario',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='securityequipment',
            name='idArea',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, related_name='SecurityEquipmentByArea', to='Empresas.Area'),
        ),
        migrations.AddField(
            model_name='empresa',
            name='id_parque',
            field=models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='Parques.Parque'),
        ),
        migrations.AddField(
            model_name='empleado',
            name='id_area',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Empresas.Area'),
        ),
        migrations.AddField(
            model_name='empleado',
            name='id_empresa',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Empresas.Empresa'),
        ),
        migrations.AddField(
            model_name='empleado',
            name='id_usuario',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='caseta',
            name='id_empresa',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Empresas.Empresa'),
        ),
        migrations.AddField(
            model_name='area',
            name='id_empresa',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Empresas.Empresa'),
        ),
        migrations.AddField(
            model_name='administrador',
            name='id_empresa',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Empresas.Empresa'),
        ),
        migrations.AddField(
            model_name='administrador',
            name='id_usuario',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='acceso',
            name='id_vigilante_ent',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='entrada', to='Empresas.Vigilante'),
        ),
        migrations.AddField(
            model_name='acceso',
            name='id_vigilante_sal',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='salida', to='Empresas.Vigilante'),
        ),
        migrations.AddField(
            model_name='acceso',
            name='invitationByUsers',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Invitaciones.InvitationByUsers'),
        ),
    ]
