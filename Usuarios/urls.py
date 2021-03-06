from django.urls import path
from .views import *

urlpatterns = [
    path('users/filter', UserViewSet.as_view({'get': 'list'})),
    path('simpleUser/filter', SimpleUserFilter.as_view({'get': 'list'})),
    path('UserPlatformCreate/', UserPlatformCreateOrList.as_view(), name='CreateUserPlatform'),
    path('UserPlatformUpdate/<pk>/', UserUpdateParcial.as_view(), name='UpdateUserPlatform'),
    path('UserPasswordUpdate/', UserPasswordUpdate.as_view(), name='UpdateUserPlatform'),
    path('UserImgUpdate/', UserImgUpdate.as_view(), name='UserImagesUpdate'),
    path('AvatarUpdate/', UserAvatarUpdate.as_view(), name='UserAvatarUpdate'),
    path('haveIneImages/', UserHaveIne.as_view(), name='UserHaveIne'),
    ## <<Actualiza un Usuario por el token>> ##
    path('partialUpdateUser/<temporalToken>/', UpdateUserPartialByToken.as_view(), name='partialUpdateUser'),
    # Obtiene un usuario por su token
    path('getUser/<temporalToken>/', getUserByToken.as_view(), name='GetUserByToken'),
    # Activa  Usuario cuando el Anfitrion confirma su Identidad, ademas le envia sus invitaciones
    path('activateUser/', activateUser.as_view(), name='ActivateUser'),
    # Activa Empleado cuando el Administrador confirma su Identida, y le envia su invitacion en caso de tener.
    #Lista los Usuarios no Activados
    path('GetUsers/NoActivated', GetUsersNotActivated.as_view({'get':'list'})),
    path('User/Delete/Devices/', DeleteFMCUserDevice.as_view()),
    # EnPoint Usado para reinciar el Password
    path('User/Reset/Passwordsita/', RestorePasswordUser.as_view()),
    # Envia alertas a todos los miembros de una compañia determinada por la sesion de un administrador o empleado
    path('SendAlert', SendAlert.as_view()),
    # Hace un downgrade de un empleado a un usuario normal.
    path('deleteEmployee/<int:idEmployee>/', DeleteEmployee.as_view()),
    # Hace un upgrade de un usuario normal a un empleado.
    path('upgradeUserEmployee/', UpgradeUserToEmployee.as_view()),
    # Crear UN PROVEEDOR
    path('createProvider/', CreateProvider.as_view()),
    path('upgradeUserToAdmin/',UpgradeUserToAdmin.as_view())

]
