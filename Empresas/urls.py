from django.urls import path
from .apiviews import EmpresaList, EmpresaDetail, EmpresaUpdate


urlpatterns = [
    path("empresas/", EmpresaList.as_view(), name="empresas_list"),
    path("empresas/<int:pk>", EmpresaDetail.as_view(), name="empresa_detail"),
    path('empresas/update/<int:pk>', EmpresaUpdate.as_view(), name='empresa_update')
]