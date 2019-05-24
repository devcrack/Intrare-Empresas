from django.urls import path
from .apiviews import *


urlpatterns = [
    path("empresas/", EmpresaList.as_view(), name="empresas_list"),
    path("empresas/<int:pk>", EmpresaDetail.as_view(), name="empresa_detail"),
    path('empresas/<int:pk>/update', EmpresaUpdate.as_view(), name='empresa_update'),

    path('administradores/', AdministradorList.as_view(), name='administradores_list'),
    path('administradores/<int:pk>', AdministradorDetail.as_view(), name='administrador_detail'),
    path('administradores/<int:pk>/update', AdministradorUpdate.as_view(), name='administrador_update'),

    path('areas/', AreaList.as_view(), name='areas_list'),
    path('areas/<int:pk>', AreaDetail.as_view(), name='area_detail'),
    path('areas/<int:pk>/update', AreaUpdate.as_view(), name='area_update'),

    path('vigilantes/', VigilanteList.as_view(), name='vigilantes_list'),
    path('vigilantes/<int:pk>', VigilanteDetail.as_view(), name='vigilante_detail'),
    path('vigilantes/<int:pk>/update', VigilanteUpdate.as_view(), name='vigilante_update'),

    path('empleados/', EmpleadoList.as_view(), name='empleados_list'),
    path('empleados/<int:pk>', EmpleadoDetail.as_view(), name='empleado_detail'),
    path('empleados/<int:pk>/update', EmpleadoUpdate.as_view(), name='empleado_update')
]