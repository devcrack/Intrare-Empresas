from django.urls import path

from .views import *

urlpatterns = [
    path('UserPlatformCreate/', UserPlatformCreateOrList.as_view(), name='CreateUserPlatform'),
    path('UserPlatformUpdate/', UserUpdateParcial.as_view(), name='UpdateUserPlatform'),
]