# Generated by Django 2.2.3 on 2019-10-10 07:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Invitaciones', '0003_auto_20191009_2013'),
    ]

    operations = [
        migrations.AlterField(
            model_name='referredinvitation',
            name='qrCode',
            field=models.CharField(blank=True, max_length=100, unique=True),
        ),
    ]
