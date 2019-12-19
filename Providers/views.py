from django.shortcuts import render
from rest_framework import generics
from .serializers import GetProviderSerializer, CustomUser

# Create your views here.

class getProviderByToken(generics.ListAPIView):
    serializer_class = GetProviderSerializer

    def get_queryset(self):
        querySet = CustomUser.objects.filter(temporalToken=self.kwargs['temporalToken'])
        return querySet