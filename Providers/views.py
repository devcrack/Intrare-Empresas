from django.shortcuts import render
from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status
from django.template.loader import render_to_string
from ControlAccs.utils import send_IntrareEmail
from secrets import token_hex
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from Usuarios.permissions import *
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
            _idProviderAdmin = _serializer.data['idUserAdminProvider']
            hostAdminUser = self.getUser(_hostId)
            if hostAdminUser is None:
                return Response(status=status.HTTP_400_BAD_REQUEST, data={'error': 'Host Admin Inexistente'})
            providerAdminUser = self.getUser(_idProviderAdmin)
            _pass = token_hex(3)
            providerUserMail = providerAdminUser.email
            providerAdminUser.set_password(_pass)
            providerAdminUser.save()
            if providerAdminUser is None:
                return Response(status=status.HTTP_400_BAD_REQUEST, data={'error': 'Admin Provider Inexistente'})

            _companyName = _serializer.data['name']
            _address = _serializer.data['companyAddress']
            _telephone = _serializer.data['telephone']
            _email = _serializer.data['email']
            _logo = _serializer.data['companyLogo']
            _webPage = _serializer.data['companyWebPage']
            _scian = _serializer.data['companyScian']
            _classification = _serializer.data['companyClassification']
            _lat = _serializer.data['companyLatitude']
            _long = _serializer.data['companyLongitude']
            _urlMap = _serializer.data['companyURLMap']
            _validity = _serializer.data['companyValidity']
            newCompany = self.createCompany(_companyName, _address, _telephone, _email, _logo, _webPage, _scian,
                                            _classification, _lat, _long, _urlMap, _validity)
            self.createAdmin(newCompany, providerAdminUser)
            admin = self.getAdmin(hostAdminUser)
            if admin is None:
                return Response(status=status.HTTP_400_BAD_REQUEST, data={'error': 'Host Admin Inexistente'})
            self.createProviderCompany(admin.id_empresa, newCompany)
            self.sendMailProviderPassword(providerUserMail, _pass)
            self.sendMailRegisteredProvider(newCompany.name, newCompany.address, hostAdminUser.email)
            return Response(status=status.HTTP_201_CREATED, data=_serializer.data)

        return Response(status=status.HTTP_400_BAD_REQUEST, data=_serializer.errors)


    @classmethod
    def getAdmin(cls, idUser):
        try:
            adminHost = Administrador.objects.get(id_usuario=idUser)
        except ObjectDoesNotExist:
            return None
        return adminHost

    @classmethod
    def getUser(cls, _id):
        try:
            usr = CustomUser.objects.get(id=_id)
        except ObjectDoesNotExist:
                return None
        return usr

    @classmethod
    def createCompany(cls,nc, addr, phone, email, logo, wp, _sc, _csf, lat, lng , urlMp, _vly):
        nwCompany = Empresa(enabled=False, name=nc, address=addr, telephone=phone, email=email,
                            logo=logo, web_page=wp, scian=_sc, classification=_csf, latitude=lat,
                            longitude=lng, url_map=urlMp, validity=_vly)
        nwCompany.save()
        return nwCompany

    @classmethod
    def createAdmin(cls, _company, _user):
        newAdmin = Administrador(id_empresa=_company, id_usuario=_user)
        newAdmin.save()
        return newAdmin

    @classmethod
    def createProviderCompany(cls, _companyHost, _companyProvider):
        newCompanyProvider = Providers(companyHost=_companyHost, companyProvider=_companyProvider)
        newCompanyProvider.save()
        return newCompanyProvider


    @classmethod
    def sendMailRegisteredProvider(cls, providerCompany, address, email):
        htmlMsg = render_to_string("registeredProvider.html", {
            "company":providerCompany,
            "address": address
        })
        send_IntrareEmail(htmlMsg, email)

    @classmethod
    def sendMailProviderPassword(cls, providerUserMail, password):
        htmlMsg = render_to_string("providerAccess.html", {
            "password": password
        })
        send_IntrareEmail(htmlMsg, providerUserMail)

class GetProvidersByHost(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated, IsAdmin]

    serializer_class = ProvidersCompanySerializer
    def get_queryset(self):
        user = self.request.user
        try:
            admin = Administrador.objects.get(id_usuario=user)
        except ObjectDoesNotExist:
            return None
        companyId = admin.id_empresa
        querySet = Providers.objects.filter(companyHost=companyId)
        return querySet

    # def list(self, request, *args, **kwargs):

