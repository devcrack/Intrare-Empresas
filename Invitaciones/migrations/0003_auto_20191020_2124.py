# Generated by Django 2.2.3 on 2019-10-21 02:24

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Invitaciones', '0002_auto_20191020_1641'),
    ]

    operations = [
        migrations.AddField(
            model_name='invitacion',
            name='urlVideo',
            field=models.CharField(max_length=300, null=True),
        ),
        migrations.AlterField(
            model_name='invitacion',
            name='dateInv',
            field=models.DateField(default=datetime.date(2019, 10, 20)),
        ),
        migrations.AlterField(
            model_name='referredinvitation',
            name='Token',
            field=models.CharField(default='7b0bbab5eeae42', max_length=14),
        ),
    ]
