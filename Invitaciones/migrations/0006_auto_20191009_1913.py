# Generated by Django 2.2.3 on 2019-10-10 00:13

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('Invitaciones', '0005_remove_invitacion_qr_code'),
    ]

    operations = [
        migrations.CreateModel(
            name='ReferredInvitation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('referredMail', models.EmailField(default=None, max_length=254)),
                ('referredPhone', models.BooleanField(default=None)),
                ('qrCode', models.CharField(max_length=100, unique=True)),
                ('referredExpiration', models.DateField()),
                ('maxForwarding', models.IntegerField(default=3)),
                ('host', models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='InvitationReferred_host', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'InvitacionesReferido',
            },
        ),
        migrations.DeleteModel(
            name='InvitacionReferido',
        ),
    ]
