from django.db import models

# Create your models here.

class Providers(models.Model):
    companyHost = models.ForeignKey('Empresas.Empresa', on_delete=models.CASCADE, related_name='iDCompanyHost')
    companyProvider = models.ForeignKey('Empresas.Empresa', on_delete=models.CASCADE, related_name='iDProvider')

    def __str__(self):
        return f"CompanyHost: {self.companyHost.name} CompanyProvider: {self.companyProvider.name}"