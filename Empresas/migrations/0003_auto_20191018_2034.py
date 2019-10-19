# Generated by Django 2.2.3 on 2019-10-19 01:34

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Empresas', '0002_auto_20191018_1842'),
    ]

    operations = [
        migrations.CreateModel(
            name='SecurityEquipment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nameEquipment', models.CharField(max_length=254, unique=True)),
                ('idArea', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, related_name='SecurityEquipmentByArea', to='Empresas.Area')),
            ],
            options={
                'verbose_name_plural': 'Equipment Security',
            },
        ),
        migrations.DeleteModel(
            name='EquipoSeguridad',
        ),
    ]
