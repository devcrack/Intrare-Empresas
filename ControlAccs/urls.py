"""ControlAccs URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, re_path
from django.urls import include, re_path
from django.conf.urls.static import static
from django.conf import settings
from fcm_django.api.rest_framework import FCMDeviceAuthorizedViewSet


admin.site.site_header = 'Administración de Intrare Industrial'


urlpatterns = [

    path('admin/', admin.site.urls),
    path('auth/', include('djoser.urls')),
    path('auth/', include('djoser.urls.authtoken')),

    path('', include('Empresas.urls')),
    path('', include('Invitaciones.urls')),
    path('', include('Parques.urls')),
    path('', include('Usuarios.urls')),
    path('', include('Grupos.urls')),
    path('', include('Bitacoras.urls')),
    path('',include('Providers.urls')),
    path('wallet/', include('Wallet.urls')),

    re_path(r'^devices?$', FCMDeviceAuthorizedViewSet.as_view({'post': 'create'}),
            name='create_fcm_device')
]

# if settings.DEBUG:
#     urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
