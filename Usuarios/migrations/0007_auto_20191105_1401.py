# Generated by Django 2.2.3 on 2019-11-05 20:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Usuarios', '0006_auto_20191030_1251'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='temporalToken',
            field=models.CharField(blank=True, max_length=12, null=True),
        ),
    ]