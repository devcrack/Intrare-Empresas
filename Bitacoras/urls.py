from django.urls import path
from .views import *


urlpatterns = [
    path('bitacora/', BitacoraListCreate.as_view(), name='bitacora_list_create'),
    path('get_bitacora/<year>/<month>/<day>/', BitacoraListGuard.as_view({'get': 'list'}), name='get_invitations_url'),
    path('firmar_salida/<int:pk>/', BitacoraUpdate.as_view(), name='firma_pase_bitacora')
]
