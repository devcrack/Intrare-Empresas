# Generated by Django 2.2.3 on 2020-01-09 20:13

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Empresas', '0006_empresa_enabled'),
    ]

    operations = [
        migrations.AlterField(
            model_name='acceso',
            name='id_vigilante_ent',
            field=models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='Ventrada', to='Empresas.Vigilante'),
        ),
        migrations.AlterField(
            model_name='acceso',
            name='id_vigilante_sal',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='Viglantesalida', to='Empresas.Vigilante'),
        ),
    ]
