# Generated by Django 2.2.3 on 2019-09-30 22:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Invitaciones', '0002_auto_20190930_1644'),
    ]

    operations = [
        migrations.AlterField(
            model_name='invitationbyusers',
            name='qr_code',
            field=models.CharField(max_length=16),
        ),
    ]
