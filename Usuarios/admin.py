from django.contrib import admin
from .models import CustomUser
from .models import UserSettings

admin.site.register(CustomUser)
admin.site.register(UserSettings)
