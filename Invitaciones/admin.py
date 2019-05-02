from django.contrib import admin

from .models import Invitacion, InvitacionTemporal, InvitacionEmpresarial
from .models import EquipoSeguridad, EquiposporInvitacion, EquipoporInvitacionesEmpresariales
from .models import EquipoporInvitacionTemporal

admin.site.register(Invitacion)
admin.site.register(InvitacionTemporal)
admin.site.register(InvitacionEmpresarial)
admin.site.register(EquipoSeguridad)
admin.site.register(EquiposporInvitacion)
admin.site.register(EquipoporInvitacionesEmpresariales)
admin.site.register(EquipoporInvitacionTemporal)
