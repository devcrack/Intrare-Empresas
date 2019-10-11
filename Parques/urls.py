from django.urls import path
from .apiviews import *

"""path


    Args:
        route: URL pattern.
        view: view function
        kwargs: Adittional arguments to pass a view function or method.
        name:  Used for pick the URL pattern out of application.
    route   
"""
urlpatterns = [
    path('parques/', ParqueList.as_view(), name='parques_list'),
    path('parques/<int:pk>/', ParqueDetail.as_view(), name='parque_detail'),
    path('parques/<int:pk>/update/', ParqueUpdate.as_view(), name='parque_update'),
]
