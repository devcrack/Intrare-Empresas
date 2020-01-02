# Generated by Django 2.2.3 on 2019-12-19 00:08

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('Empresas', '0006_empresa_enabled'),
    ]

    operations = [
        migrations.CreateModel(
            name='Providers',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('companyHost', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='iDCompanyHost', to='Empresas.Empresa')),
                ('companyProvider', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='iDProvider', to='Empresas.Empresa')),
            ],
        ),
    ]