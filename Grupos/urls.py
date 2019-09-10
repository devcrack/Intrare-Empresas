from django.urls import path
from .views import *


urlpatterns = [
    path('grupos/contactos/', ContactoList.as_view(), name='contacto_list'),
    path('grupos/contactos/<int:pk>/', ContactoDetail.as_view(), name='contacto_detail'),
    path('grupos/contactos/<int:pk>/update/', ContactoUpdate.as_view(), name='contacto_update'),
]
