# Generated by Django 2.2.3 on 2019-10-19 19:07

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('Invitaciones', '0001_initial'),
        ('Empresas', '0002_auto_20191019_1407'),
    ]

    operations = [
        migrations.AddField(
            model_name='referredinvitation',
            name='host',
            field=models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='InvitationReferred_host', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='referredinvitation',
            name='id_empresa',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='id_company_ReferredInv', to='Empresas.Empresa'),
        ),
        migrations.AddField(
            model_name='invitationbyusers',
            name='host',
            field=models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='Invitation_host', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='invitationbyusers',
            name='idGuest',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='Invitation_guest', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='invitationbyusers',
            name='idInvitation',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='InvitationLINK', to='Invitaciones.Invitacion'),
        ),
        migrations.AddField(
            model_name='invitacion',
            name='id_area',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Empresas.Area'),
        ),
        migrations.AddField(
            model_name='invitacion',
            name='id_empresa',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='id_company_inv', to='Empresas.Empresa'),
        ),
    ]
