from django.urls import path

from .views import *

urlpatterns = [
    path('users/filter', UserViewSet.as_view({'get': 'list'})),
    path('UserPlatformCreate/', UserPlatformCreateOrList.as_view(), name='CreateUserPlatform'),
    path('UserPlatformUpdate/<pk>/', UserUpdateParcial.as_view(), name='UpdateUserPlatform'),
    path('UserPasswordUpdate/', UserPasswordUpdate.as_view(), name='UpdateUserPlatform'),
    path('UserImgUpdate/', UserImgUpdate.as_view(), name='UserImagesUpdate'),
    path('AvatarUpdate/', UserAvatarUpdate.as_view(), name='UserAvatarUpdate'),
    path('haveIneImages/', UserHaveIne.as_view(), name='UserHaveIne'),
    path('partialUpdateUser/<temporalToken>/', UpdateUserPartialByToken.as_view(), name='partialUpdateUser'),
    path('getUser/<temporalToken>/', getUserByToken.as_view(), name='GetUserByToken'),
    #Activa a un determinado Usuario
    path('activateUser/', activateUser.as_view(), name='ActivateUser'),
    #Lista los Usuarios no Activados
    path('GetUsers/NoActivated', GetUsersNotActivated.as_view({'get':'list'})),
    path('User/Delete/Devices/', DeleteFMCUserDevice.as_view()),
    path('User/Reset/Passwordsita/', RestorePasswordUser.as_view())
]