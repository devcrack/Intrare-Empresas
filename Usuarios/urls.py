from django.urls import path, re_path

from .views import *

urlpatterns = [
    path('users/filter', UserViewSet.as_view({'get': 'list'})),
    path('UserPlatformCreate/', UserPlatformCreateOrList.as_view(), name='CreateUserPlatform'),
    # Se utilizara normalmente en la app
    # path('UserPlatformUpdateLogged/', UserUpdateParcial.as_view()),
    # Se utilizara cuando el usuario complete su preregistro, la busqueda del registro a modificar se hara mediante
    # el email
    # path('UserPlatformUpdateNoLogged/', UserUpdateParcial.as_view()),
    path('UserPlatformUpdate/', UserUpdateParcial.as_view(), name='UpdateUserPlatform'),
    path('UserPasswordUpdate/', UserPasswordUpdate.as_view(), name='UpdateUserPlatform'),
    path('UserImgUpdate/', UserImgUpdate.as_view(), name='UserImagesUpdate'),
    path('AvatarUpdate/', UserAvatarUpdate.as_view(), name='UserAvatarUpdate'),
    path('haveIneImages/', UserHaveIne.as_view(), name='UserHaveIne'),
    path('partialUpdateUser/<temporalToken>/', UpdateUserPartialByToken.as_view(), name='partialUpdateUser' )
]