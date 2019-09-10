from django.urls import path

from .views import *

urlpatterns = [
    path('UserPlatformCreate/', UserPlatformCreateOrList.as_view(), name='CreateUserPlatform'),
    path('UserPlatformUpdate/', UserUpdateParcial.as_view(), name='UpdateUserPlatform'),
    path('UserPasswordUpdate/', UserPasswordUpdate.as_view(), name='UpdateUserPlatform'),
    path('UserImgUpdate/', UserImgUpdate.as_view(), name = 'UserImagesUpdate'),
    path('AvatarUpdate/', UserAvatarUpdate.as_view(), name = 'UserAvatarUpdate'),
]