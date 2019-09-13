# Generated by Django 2.2.3 on 2019-09-13 17:18

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Grupos', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='grupo_has_contacto',
            name='id_contacto',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.DeleteModel(
            name='Contacto',
        ),
    ]
