# Generated by Django 2.2.3 on 2019-11-05 20:01

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Invitaciones', '0006_auto_20191030_1250'),
    ]

    operations = [
        migrations.AlterField(
            model_name='referredinvitation',
            name='expiration',
            field=models.DateField(default=datetime.date(2019, 11, 6)),
        ),
    ]
