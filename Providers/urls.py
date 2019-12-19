from django.urls import path

from .views import *


urlpatterns = [
    path('getProvider/<temporalToken>/', getProviderByToken.as_view()),
    ]
