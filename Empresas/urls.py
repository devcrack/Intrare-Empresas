from django.urls import path
from .apiviews import EmpresaList, EmpresaDetail


urlpatterns = [
    path("empresas/", EmpresaList.as_view(), name="empresas_list"),
    path("empresas/<int:pk>", EmpresaDetail.as_view(), name="empresa_detail")
]