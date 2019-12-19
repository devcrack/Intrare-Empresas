from django.urls import path

from .views import *


urlpatterns = [
    path('getProvider/<temporalToken>/', getProviderByToken.as_view()),
    path('updateProvider/<temporalToken>/', updatePartialProvider.as_view()),
    path('createCompanyProvider', AddCompanyProvider.as_view()),
    ]
