from django.urls import path
from .apiviews import *
from rest_framework.routers import DefaultRouter
from .apiviews import EmpresaViewSet

router = DefaultRouter()
router.register('empresas', EmpresaViewSet, base_name='empresas')

urlpatterns = [
    path("empresas/", EmpresaList.as_view(), name="empresas_list"),
    path("empresas/<int:pk>/", EmpresaDetail.as_view(), name="empresa_detail"),
    path('empresas/<int:pk>/update/', EmpresaUpdate.as_view(), name='empresa_update'),

    path('empresas/<int:pk>/areas/', AreaList.as_view(), name="area_list"),
    path('empresas/<int:pk>/vigilantes/', VigilanteList.as_view(), name='vigilante_list'),
    path('empresas/<int:pk>/empleados/', EmpleadoList.as_view(), name='empleado_list'),
    path('empresas/<int:pk>/area/<int:pk_area>/empleados/', EmpleadoEmpresaXArea.as_view(), name='empleado_empresa_area_list'),

    path('empresas/administradores/', AdministradorList.as_view(), name='administradores_list'),
    path('empresas/administradores/<int:pk>/', AdministradorDetail.as_view(), name='administrador_detail'),
    path('empresas/administradores/<int:pk>/update/', AdministradorUpdate.as_view(), name='administrador_update'),

    path('empresas/areas/', AreaListAll.as_view(), name='areas_list'),
    path('empresas/areas/<int:pk>/', AreaDetail.as_view(), name='area_detail'),
    path('empresas/areas/<int:pk>/update/', AreaUpdate.as_view(), name='area_update'),

    path('empresas/vigilantes/', VigilanteListAll.as_view(), name='vigilantes_list'),
    path('empresas/vigilantes/<int:pk>/', VigilanteDetail.as_view(), name='vigilante_detail'),
    path('empresas/vigilantes/<int:pk>/update/', VigilanteUpdate.as_view(), name='vigilante_update'),

    path('empresas/empleados/', EmpleadoListAll.as_view(), name='empleados_list'),
    path('empresas/empleados/<int:pk>/', EmpleadoDetail.as_view(), name='empleado_detail'),
    path('empresas/empleados/<int:pk>/update/', EmpleadoUpdate.as_view(), name='empleado_update')
]

urlpatterns += router.urls