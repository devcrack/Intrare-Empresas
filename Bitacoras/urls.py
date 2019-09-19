from django.urls import path
from .views import *


urlpatterns = [
    path('bitacora/', BitacoraListCreate.as_view(), name='bitacora_list_create'),

]
