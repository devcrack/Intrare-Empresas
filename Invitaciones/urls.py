from django.urls import path
from rest_framework.routers import DefaultRouter

from .Apiviews import *

"""path


    Args:
        route: URL pattern.
        view: view function
        kwargs: Adittional arguments to pass a view function or method.
        name:  Used for pick the URL pattern out of application.
    route   
"""
urlpatterns = [
    path('invitaciones/', Invitacion_List.as_view(), name='invitaciones_url')  # path(route, view, kwargs, name= None)]
]
