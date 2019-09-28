from django.urls import path
from .views import *


urlpatterns = [
    path('grupos', GrupoList.as_view(), name='grupo_list'),
    path('grupos/<int:pk>', GrupoDetail.as_view(), name='grupo_detail'),
    path('grupos/<int:pk>/update', GrupoUpdate.as_view(), name='grupo_update'),
    path('grupos/<int:pk>/delete', GrupoDelete.as_view(), name='grupo_delete'),

    path('grupos/contacts_grupo', ContactosXGrupoCreate.as_view(), name='contactos_x_grupo_create'),
    path('grupos/contacts_grupos/<int:id_grupo>', ContactosXGrupoList.as_view(), name='contactos_x_grupo_list'),
    path('grupos/contacts_grupos/<int:id_grupo>/delete/<int:id_user>', ContactosXGrupoDelete.as_view(), name='contactos_x_grupo_delete'),


    #path('grupos/contacts_grupos/delete/<int:pk>/', ContactosXGrupoDelete.as_view(), name='contactos_x_grupo_delete'),
]
