from django.urls import path
from .views import GetWallet


urlpatterns = [
    path('create/<str:qrcode>/<int:id>', GetWallet.as_view(), name='get_wallet'),
]