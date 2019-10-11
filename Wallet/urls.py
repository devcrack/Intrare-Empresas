from django.urls import path
from .views import GetWallet


urlpatterns = [
    path('create/<str:qrcode>', GetWallet.as_view(), name='get_wallet'),
]