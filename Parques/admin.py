from django.contrib import admin
from .models import AccesoParque, Parque, VigilanteParque

admin.site.register(AccesoParque)
admin.site.register(Parque)
admin.site.register(VigilanteParque)