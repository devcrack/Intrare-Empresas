from django.shortcuts import render
from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status

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
        self.serializer_class = CreateCompanyProviderSerializer
        _serializer = self.serializer_class(data=request.data)
        if _serializer.is_valid():
            _serializer.save()
            _hostId = _serializer.data['host']
            return Response(status=status.HTTP_201_CREATED, data=_serializer.data)
        return Response(status=status.HTTP_400_BAD_REQUEST, data=_serializer.errors)
            #Notificar HOST que el proveedor se ha dado de alta exitosamente.

    @classmethod
    def createCompany(cls,nc, addr, phone, email, logo, wp, _sc, _csf, lat, lng , urlMp, _vly):
        nwCompany = Empresa(enabled=False, name=nc, address=addr, telephone=phone, email=email,
                            logo=logo, web_page=wp, scian=_sc, classification=_csf, latitude=lat,
                            longitude=lng, url_map=urlMp, validity=_vly)
        nwCompany.save()
