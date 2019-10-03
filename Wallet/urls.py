from django.urls import path
from .views import GetWallet


urlpatterns = [
    path('create', GetWallet.as_view(), name='get_wallet'),
]