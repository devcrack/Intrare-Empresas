from django.contrib import admin

from .models import *

admin.site.register(Empresa)
admin.site.register(Administrador)
admin.site.register(Empleado)
admin.site.register(Vigilante)
admin.site.register(Area)
admin.site.register(Caseta)
admin.site.register(Veto)
admin.site.register(Acceso)
admin.site.register(SecurityEquipment)