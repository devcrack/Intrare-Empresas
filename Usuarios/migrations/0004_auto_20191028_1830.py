# Generated by Django 2.2.3 on 2019-10-29 00:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Usuarios', '0003_auto_20191028_1655'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='temporalToken',
            field=models.CharField(blank=True, default='9677401381', max_length=10, null=True),
        ),
    ]
