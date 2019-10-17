# Generated by Django 2.2.3 on 2019-10-16 00:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Invitaciones', '0005_auto_20191015_1902'),
    ]

    operations = [
        migrations.RenameField(
            model_name='referredinvitation',
            old_name='subject',
            new_name='asunto',
        ),
        migrations.RenameField(
            model_name='referredinvitation',
            old_name='vehicle',
            new_name='automovil',
        ),
        migrations.RenameField(
            model_name='referredinvitation',
            old_name='companyFrom',
            new_name='empresa',
        ),
        migrations.RenameField(
            model_name='referredinvitation',
            old_name='dateSend',
            new_name='fecha_hora_envio',
        ),
        migrations.RenameField(
            model_name='referredinvitation',
            old_name='idArea',
            new_name='id_area',
        ),
        migrations.RenameField(
            model_name='referredinvitation',
            old_name='idCompany',
            new_name='id_empresa',
        ),
        migrations.RenameField(
            model_name='referredinvitation',
            old_name='notes',
            new_name='notas',
        ),
        migrations.AlterField(
            model_name='referredinvitation',
            name='Token',
            field=models.CharField(default='1de4462079a049', max_length=14),
        ),
    ]