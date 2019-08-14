from django.urls import path
from rest_framework.routers import DefaultRouter

from .views import *

"""path


    Args:
        route: URL pattern.
        view: view function
        kwargs: Adittional arguments to pass a view function or method.
        name:  Used for pick the URL pattern out of application.
    route   
"""
urlpatterns = [
    path('get_inv/', InvitationListAdminEmployee.as_view({'get': 'list'}), name='get_invitations_url'),  # path(route, view, kwargs, name= None)]
    path('get_inv/user', InvitationListUser.as_view({'get': 'list'}), name='get_inv_user'),
    path('create_inv/', InvitationCreate.as_view(), name='create_invitations_url'),  # path(route, view, kwargs, name= None
    path('equipo_seguridad/', EquipoSeguridadList.as_view(), name='equipo_seguridad_list')
]
