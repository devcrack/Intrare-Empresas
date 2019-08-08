from django.contrib import admin

from .models import EquipoSeguridad, EquiposporInvitacion
from .models import Invitacion
admin.site.register(Invitacion)
admin.site.register(EquipoSeguridad)
admin.site.register(EquiposporInvitacion)
