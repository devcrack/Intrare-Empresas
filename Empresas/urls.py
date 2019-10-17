from django.urls import path
from .apiviews import *
from rest_framework.routers import DefaultRouter
from .apiviews import EmpresaViewSet
from .views import *



router = DefaultRouter()
router.register('empresas', EmpresaViewSet, base_name='empresas')

urlpatterns = [
    path("empresas/", EmpresaList.as_view(), name="empresas_list"),
    path("empresas/<int:pk>/", EmpresaDetail.as_view(), name="empresa_detail"),
    path('empresas/<int:pk>/update/', EmpresaUpdate.as_view(), name='empresa_update'),
    path('empresas/filter', EmpresaViewSet.as_view({'get': 'list'})),

    path('empresas/administradores/', AdministradorList.as_view(), name='administradores_list'),
    path('empresas/administradores/<int:pk>/', AdministradorDetail.as_view(), name='administrador_detail'),
    path('empresas/administradores/user/<int:pk_user>/', AdministradorDetailUser.as_view(), name='administrador_detail_user'),
    path('empresas/administradores/<int:pk>/update/', AdministradorUpdate.as_view(), name='administrador_update'),
    path('empresas/administradoresByCompany/<int:id_company>', AdministradoresViewSet.as_view({'get': 'list'})),

    path('empresas/areas/', AreaListAll.as_view(), name='areas_list'),
    path('empresas/areas/<int:pk>/', AreaDetail.as_view(), name='area_detail'),
    path('empresas/areas/<int:pk>/update/', AreaUpdate.as_view(), name='area_update'),

    path('empresas/vigilantes/', VigilanteListAll.as_view(), name='vigilantes_list'),
    path('empresas/vigilantes/<int:pk>/', VigilanteDetail.as_view(), name='vigilante_detail'),
    path('empresas/vigilante/user/<int:pk_user>/', VigilanteDetailUser.as_view(), name='vigilante_detail_user'),
    path('empresas/vigilantes/<int:pk>/update/', VigilanteUpdate.as_view(), name='vigilante_update'),

    path('empresas/empleados/', EmpleadoListAll.as_view(), name='empleados_list'),
    path('empresas/empleados/<int:pk>/', EmpleadoDetail.as_view(), name='empleado_detail'),
    path('empresas/empleados/user/<int:pk_user>/', EmpleadoDetailUser.as_view(), name='empleado_detail_user'),
    path('empresas/empleados/<int:pk>/update/', EmpleadoUpdate.as_view(), name='empleado_update'),
    # Obtiene todos los empleados activos de la Empresa por Django Filter (celular, email)
    path('empresas/empleados/filter', EmpleadosViewSet.as_view({'get': 'list'})),

    path('empresas/casetas/', CasetaListAll.as_view(), name='casetas_list'),
    path('empresas/casetas/<int:pk>/', CasetaDetail.as_view(), name='caseta_list'),
    path('empresas/casetas/<int:pk>/update/', CasetaUpdate.as_view(), name='caseta_update'),

    path('empresas/<int:pk>/area/<int:pk_area>/empleados/', EmpleadoEmpresaXArea.as_view(), name='empleado_empresa_area_list'),

    path("empresas/accesos/", AccesoList.as_view(), name="accesos_list"),  # Listado de todos los accesos
    path('empresas/accesos/search/<str:qr_code>/', AccessListToGuard.as_view({'get': 'list'}), name='get_inv_qrcode_guard'), # Obtiene Acceso por codigo QR
    # Obtiene Acceso por id_Acceso
    path('empresas/accesos/search/<int:pk>', AccessListToAdminAndEmployee.as_view({'get': 'list'}), name='get_inv_qrcode_guard'),
    path('empresas/access/create', AccessCreate.as_view(), name='_createacces'),  #
    #Actualiza el pase de salida , es decir lo FIRMA
    path('empresas/access/update/exitpass/<int:pk>/', AccessUpdateExitPass.as_view(), name='accessUpdate1'),
    #Actualiza el pase de salida del acceso pero los Filtra por QR.
    path('empresas/access/update/forExit/<qr_code>/', AccessUpdateData.as_view(), name='accessUpdate1'),
    path('empresas/access/getAcc/by/date/', get_accestoEnterByDate.as_view({'get': 'list'}), name='getAccessbyDate'),
    path('empresas/access/getAccs/<year>/<month>/<day>/', get_accestoEnterByDate.as_view({'get': 'list'}), name='getAccSession'),
    # Nootificar firmar pase de salida
    path('notifySignExitPass/<int:idAcc>/', NotifyHostSignPass.as_view()),
    #Obtiene todos los accesos que ha realizado un Administrador o un Empleado. Determina quien es por la sesion.
    path('getAccessBySession/', GetAccessBySession.as_view({'get':'list'})),
    # path('empresas/access/getAccs/', AccessListGet.as_view({'get': 'list'}), name='getAccSession')
]

urlpatterns += router.urls