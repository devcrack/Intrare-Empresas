from django.contrib import admin

from .models import Empresa, Administrador, Empleado
from .models import Vigilante, Area, Caseta, Veto
from .models import Acceso

admin.site.register(Empresa)
admin.site.register(Administrador)
admin.site.register(Empleado)
admin.site.register(Vigilante)
admin.site.register(Area)
admin.site.register(Caseta)
admin.site.register(Veto)
admin.site.register(Acceso)
