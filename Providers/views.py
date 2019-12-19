from django.shortcuts import render
from rest_framework import generics
from .serializers import *

# Create your views here.

class getProviderByToken(generics.ListAPIView):
    serializer_class = ProviderSerializer

    def get_queryset(self):
        querySet = CustomUser.objects.filter(temporalToken=self.kwargs['temporalToken'])
        return querySet

class updatePartialProvider(generics.UpdateAPIView):
    queryset = CustomUser.objects.all()
    lookup_field = 'temporalToken'
    serializer_class = UpdateProviderSerializer

    def patch(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)

class AddCompanyProvider(generics.CreateAPIView):
    def create(self, request, *args, **kwargs):
        pass