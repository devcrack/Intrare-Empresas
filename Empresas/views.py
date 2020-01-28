from rest_framework import generics, viewsets
from rest_framework.response import Response
from rest_framework import status
from django.core.exceptions import ObjectDoesNotExist
from rest_framework.permissions import IsAuthenticated
from fcm_django.models import FCMDevice
import datetime
from datetime import date
from django.utils import timezone

from Empresas.models import Acceso
from Usuarios.permissions import *
from .serializers import *
from django.utils import timezone
from Invitaciones.models import Invitacion, InvitationByUsers
from Empresas.models import Vigilante
from django.template.loader import render_to_string
from ControlAccs.utils import send_sms, send_IntrareEmail, sendPushNotificationIntrare



class AccessCreate(generics.CreateAPIView):
    """ Generacion de Accesso. NOTIFICAR a ANFITRION cuando INVITADO llegue"""
    permission_classes = (IsAuthenticated, isGuard,)

    def create(self, request, *args, **kwargs):
        """
        POST
        Creamos un acceso a partir de los siguientes parametros:
            - id_vigilante_ent: Se obtiene de la session actual
            - datos_coche: Puede ser Nulo
            - qr_code : NO puede ser nulo

        JSON
        {
            "datos_coche":null,
            "qr_code": "4fa0d6e85e5011be"
        }
        """
        self.serializer_class = AccessCreateSerializer
        _serializer = self.serializer_class(data=request.data)
        if _serializer.is_valid():
            _serializer.save()
            _guard_ent = Vigilante.objects.filter(id_usuario=self.request.user)[0]
            _currentCompany = _guard_ent.id_empresa

            ## <<Cargando Datos de JSON>>##
            _datos_coche = _serializer.data['datos_coche']
            _qr_code = _serializer.data['qr_code']
            try:
                _invByUsers = InvitationByUsers.objects.get(qr_code=_qr_code)
            except ObjectDoesNotExist:
                return Response(status=status.HTTP_400_BAD_REQUEST, data={'Error': 'Invitacion Corrompida'})
            ## <<Cargando Fecha Actual>> ##
            _currentDate = date(year=timezone.datetime.now().year, month=timezone.datetime.now().month,
                                day=timezone.datetime.now().day)
            ## << Cargando datos Invitacion>>
            _typeInv = _invByUsers.idInvitation.typeInv
            _guest = _invByUsers.idGuest
            _companyHost = _invByUsers.idInvitation.id_empresa # Empresa que invita a esta persona.
            if _currentCompany.id is not _companyHost.id:
                return Response(status=status.HTTP_401_UNAUTHORIZED,
                                data={"error": "!ACCESO NEGADO¡. Este invitado no ha sido Invitado por la Empresa"})
            if _typeInv == 2: # Invitacion Recurrente
                _expiration = _invByUsers.idInvitation.expiration
                _diary = _invByUsers.idInvitation.diary
                _weekDay = str(timezone.datetime.now().weekday())
                if _currentDate > _expiration: # La invitacion esta en fecha
                    return Response(status=status.HTTP_401_UNAUTHORIZED,
                                    data={"error": "!ACCESO NEGADO¡. Esta invitacion ha expirado."})
                if _weekDay not in _diary: # El dia de la invitacion es el correcto
                    return Response(status=status.HTTP_401_UNAUTHORIZED,
                                    data={"error": "!ACCESO NEGADO¡. No esta autorizado para este dia."})
            else:  # Invitaciones Normales y Empresariales
                ## <<Verificandop si la invitacion ha sido confirmada>>
                if not _invByUsers.confirmed:
                    return Response(status=status.HTTP_401_UNAUTHORIZED,
                                    data={"error": "!ACCESO NEGADO¡. Este invitado no ha confirmado la invitación"})
                _dateInv = _invByUsers.idInvitation.dateInv
                if _currentDate != _dateInv:
                    return Response(status=status.HTTP_401_UNAUTHORIZED,
                                    data={"error": "!ACCESO NEGADO¡.Esta invitacion esta fuera de fecha."})
            _timeInv = _invByUsers.idInvitation.timeInv
            _currentHour = timezone.datetime.now().hour
            _currentMinute = timezone.datetime.now().minute
            _currentTime = datetime.time(_currentHour, _currentMinute)

            _host = _invByUsers.host

            if _currentTime > _timeInv:
                _nameGuest = _guest.first_name + " " + _guest.last_name
                msgHeader = f"Tu invitado {_nameGuest} ha llegado tarde."
                msgMail = "Ponte en contacto con tu invitado  y/o modifica la hora de acceso"
                sendPushNotificationIntrare(_host, msgHeader)
                html_message = render_to_string("genericEmail.html", {"messageHeader": msgHeader,
                                                                      "msg": msgMail})
                send_IntrareEmail(html_message, _host.email)
                return Response(status=status.HTTP_401_UNAUTHORIZED,
                                data={"error": "El invitado ha llegado tarde. Acceso Negado"})

            self.createAcces(_guard_ent, _invByUsers, _datos_coche, _qr_code)
            ## <<Enviar Correo y SMS>> ##
            # _host = _invByUsers.host  # Modifiacion 27 -01
            _guestFullName = _invByUsers.idGuest.first_name + " " + _invByUsers.idGuest.last_name
            _emailHost = _host.email
            _cellphoneHost = _host.celular
            _hostDevices = FCMDevice.objects.filter(user=_host)
            _from = _invByUsers.idInvitation.empresa
            _msg = "Tu invitado " + _guestFullName + " proveniente de: " + _from+  " ha llegado"
            html_message = render_to_string('guestArrived.html',
                                            { 'guestName':_guestFullName,
                                              'from':_from
                                            })
            if len(_hostDevices) > 0: # Envio NOTIFICACION  PUSH
                _hostDevices.send_message(title="Intrare", body=_msg, sound="Default")
            send_IntrareEmail(html_message, _emailHost) # Envio Notificacion EMAIL
            send_sms(_cellphoneHost, _msg)  # Envio Notificacion SMS
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST, data=_serializer.errors)
        return Response(status=status.HTTP_201_CREATED)

    @classmethod
    def createAcces(cls, _guard_ent, _invByUsers, _vehicleData, _qr_code):
        _errorResponse = None
        nwAccess = Acceso(id_vigilante_ent=_guard_ent, invitationByUsers=_invByUsers, datos_coche=_vehicleData, qr_code=_qr_code)
        nwAccess.save()


class AccessUpdateExitPass(generics.UpdateAPIView):
    """
    FIRMAR Pase de salida por el Anfitrion
    """
    queryset = Acceso.objects.all()
    serializer_class = AccesUpdateSerializer
    lookup_field = 'pk'


    def update(self, request, *args, **kwargs):
        """
        PATCH
        JSON
        {
	        "pase_salida":false
        }
        """
        instance = self.get_object()
        instance.pase_salida = request.data.get('pase_salida')
        instance.save()
        return Response(status=status.HTTP_202_ACCEPTED)


class AccessUpdateData(generics.UpdateAPIView):
    """
    Actualiza el acceso cuando va a salir el invitado. EndPoint Usado por el Guardia.
    PATCH
    JSON
    {
	    "estado":2,
	    "motivo_no_firma":null,
	    "comentarios_VE":"todo bien"
    }
    """
    queryset = Acceso.objects.all()
    serializer_class = AccesUpdateSerializer
    lookup_field = 'qr_code'
    permission_classes = (IsAuthenticated, isGuard,)

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        _guard_exit = Vigilante.objects.filter(id_usuario=self.request.user)[0]
        instance.id_vigilante_sal = _guard_exit
        instance.fecha_hora_salida = timezone.datetime.now()
        instance.estado = request.data.get('estado')
        instance.motivo_no_firma = request.data.get('motivo_no_firma')
        instance.comentarios_VE = request.data.get('comentarios_VE')
        instance.save()
        return Response(status=status.HTTP_202_ACCEPTED)


class AccessListGet(viewsets.ModelViewSet):
    #Obtiene una lista de TODOS los accesos
    permission_classes = (IsAuthenticated, IsAdmin | IsEmployee | isGuard,)  # The user logged have to be and admin, employee or Guard

    def list(self, request, *args, **kwargs):
        self.queryset = Acceso.objects.all()
        _nReg = len(self.queryset)

        if _nReg > 0:
            queryset = self.queryset
            _serializer = AccessDetail(queryset, many=True)
            return Response(_serializer.data)
        else:
            return Response(status=status.HTTP_204_NO_CONTENT)


class get_accestoEnterByDate(viewsets.ModelViewSet):

    permission_classes = (IsAuthenticated, IsAdmin | IsEmployee | isGuard,)

    def get_queryset(self):
        usr = self.request.user
        _idCompany = None

        if usr.roll == settings.ADMIN:
            _admCompany = Administrador.objects.filter(id_usuario=usr)[0]
            _idCompany = _admCompany.id_empresa
            queryset=Acceso.objects.filter(invitationByUsers__idInvitation__id_empresa=_idCompany)
        if usr.roll == settings.EMPLEADO:
            _employee = Empleado.objects.filter(id_usuario=usr)[0]
            _idCompany = _employee.id_empresa
            queryset = Acceso.objects.filter(invitationByUsers__idInvitation__id_empresa=_idCompany,
                                             invitationByUsers__host=usr)
        if usr.roll == settings.VIGILANTE:
            _guard = Vigilante.objects.filter(id_usuario=usr)[0]
            _idCompany = _guard.id_empresa
            queryset = Acceso.objects.filter(invitationByUsers__idInvitation__id_empresa=_idCompany)

        y = self.kwargs['year']
        m = self.kwargs['month']
        d = self.kwargs['day']
        queryset = queryset.filter(fecha_hora_acceso__year=y,
                                   fecha_hora_acceso__month=m,
                                   fecha_hora_acceso__day=d)
        return queryset

    def list(self, request, *args, **kwargs):
        _queryset = self.get_queryset()
        _nReg = len(_queryset)

        if _nReg > 0:
            _serializer = AccessDetail(_queryset, many=True)
            return Response(_serializer.data)
        else:
            return Response(status=status.HTTP_204_NO_CONTENT)


class GetAccessEnterByDateRange(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated, IsAdmin | IsEmployee | isGuard,)

    def get_queryset(self):
        usr = self.request.user
        _idCompany = None

        if usr.roll == settings.ADMIN:
            _admCompany = Administrador.objects.filter(id_usuario=usr)[0]
            _idCompany = _admCompany.id_empresa
            queryset=Acceso.objects.filter(invitationByUsers__idInvitation__id_empresa=_idCompany)
        if usr.roll == settings.EMPLEADO:
            _employee = Empleado.objects.filter(id_usuario=usr)[0]
            _idCompany = _employee.id_empresa
            queryset = Acceso.objects.filter(invitationByUsers__idInvitation__id_empresa=_idCompany,
                                             invitationByUsers__host=usr)
        if usr.roll == settings.VIGILANTE:
            _guard = Vigilante.objects.filter(id_usuario=usr)[0]
            _idCompany = _guard.id_empresa
            queryset = Acceso.objects.filter(invitationByUsers__idInvitation__id_empresa=_idCompany)

        y1 = self.kwargs['year1']
        m1 = self.kwargs['month1']
        d1 = self.kwargs['day1']
        y2 = self.kwargs['year2']
        m2 = self.kwargs['month2']
        d2 = self.kwargs['day2']

        iniDate = y1 + "-" + m1 + "-" + d1
        finalDate = y2 + "-" + m2 + "-" + d2

        queryset = queryset.filter(fecha_hora_acceso__range=[iniDate, finalDate])

        return queryset


    def list(self, request, *args, **kwargs):
        _queryset = self.get_queryset()
        _nReg = len(_queryset)

        if _nReg > 0:
            _serializer = AccessDetail(_queryset, many=True)
            return Response(_serializer.data)
        else:
            return Response(status=status.HTTP_204_NO_CONTENT)


class AccessListToGuard(viewsets.ModelViewSet):
    """
    Lista los Accesos por Codigo QR
    """
    permission_classes = (isGuard,)

    def list(self, request, *args, **kwargs):
        qr_code = self.kwargs['qr_code']

        self.queryset = Acceso.objects.filter(qr_code=qr_code)
        _nReg = len(self.queryset)
        if _nReg > 0:
            print('nReg=', _nReg)
            queryset = self.queryset
            _serializer = AccessSerializer(queryset, many=True)
            return Response(_serializer.data)
        else:
            return Response(status=status.HTTP_204_NO_CONTENT)


class AccessListToAdminAndEmployee(viewsets.ModelViewSet):
    """
    Lista el Acceso por id_Acceso
    """
    permission_classes = (isAdmin | isEmployee,)

    def list(self, request, *args, **kwargs):
        a_pk = self.kwargs['pk']

        self.queryset = Acceso.objects.filter(id=a_pk)
        _nReg = len(self.queryset)
        if _nReg > 0:
            print('nReg=', _nReg)
            queryset = self.queryset
            _serializer = AccessDetailFull(queryset, many=True, context={"request": request})
            return Response(_serializer.data)
        else:
            return Response(status=status.HTTP_204_NO_CONTENT)


class NotifyHostSignPass(generics.ListAPIView):
    def get(self, request, *args, **kwargs):
        _idAcc = self.kwargs['idAcc']
        acc = None
        try:
            acc =Acceso.objects.get(id=_idAcc)
        except ObjectDoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND, data={"error":"Acceso no Encontrado"})
        _host = acc.invitationByUsers.host
        _hostDevice = FCMDevice.objects.filter(user=_host)
        _emailHost = _host.email
        _cellphoneHost = _host.celular

        _guest = acc.invitationByUsers.idGuest
        _guestFullName = _guest.first_name + " " + _guest.last_name
        _dateTimeAcc = str(acc.fecha_hora_acceso.strftime("%Y/%m/%d, %H:%M"))
        _msg = "Firma el pase de salida del Invitado: " + _guestFullName + "\nFecha y Hora de Acceso:" + _dateTimeAcc
        html_message = render_to_string('notifyHostSigAccess.html',
                                        { 'guestName': _guestFullName,
                                          'dateTimeAcc': _dateTimeAcc
                                        })
        if len(_hostDevice) > 0:
            _hostDevice.send_message(title="Intrare", body=_msg, sound="Default")
        send_IntrareEmail(html_message, _emailHost)
        send_sms(_cellphoneHost, _msg)
        return Response(status=status.HTTP_200_OK)


class GetAccessBySession(viewsets.ModelViewSet):
    """
    Obtiene los Accesos por Session.
    """
    permission_classes = (IsAuthenticated,IsAdmin | IsEmployee,)

    def get_queryset(self):
        usr = self.request.user
        queryset = Acceso.objects.filter(invitationByUsers__host=usr)
        return queryset

    def list(self, request, *args, **kwargs):
        _queryset = self.get_queryset()
        _nReg = len(_queryset)
        if _nReg > 0:
            _serializer = AccessDetail(_queryset, many=True)
            return Response(_serializer.data)
        else:
            return Response(status=status.HTTP_204_NO_CONTENT)


class AddSecurityEquipment(generics.CreateAPIView, generics.DestroyAPIView):
    permission_classes = [IsAuthenticated, IsAdmin]

    def create(self, request, *args, **kwargs):
        self.serializer_class = SecurityEquipmentSerializer
        _serializer = self.serializer_class(data=request.data)
        if _serializer.is_valid():
            _serializer.save()
            return Response(status=status.HTTP_201_CREATED)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST, data=_serializer.errors)

    def delete(self, request, *args, **kwargs):
        return None


class UpdateSecurityEquipment(generics.UpdateAPIView):
    permission_classes = [IsAuthenticated, IsAdmin]

    queryset = SecurityEquipment.objects.all()
    serializer_class = SecurityEquipmentSerializer
    lookup_field = 'pk'

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.nameEquipment = request.data.get('nameEquipment')
        instance.save()
        return Response(status=status.HTTP_202_ACCEPTED)


class DeleteSecurityEquipment(generics.DestroyAPIView):
    permission_classes = [IsAuthenticated, IsAdmin]

    queryset = SecurityEquipment.objects.all()
    serializer_class = SecurityEquipmentSerializer
    lookup_field = 'pk'

    def delete(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.delete()
        return Response(status=status.HTTP_202_ACCEPTED)


class GetSecEquByArea(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated, IsAdmin]

    def list(self, request, *args, **kwargs):
        _idArea = self.kwargs['idArea']
        _secEquByArea = SecurityEquipment.objects.filter(idArea=_idArea)
        if  len(_secEquByArea) > 0:
            _serializer = SecurityEquipmentSerializer(_secEquByArea, many=True)
            return Response(_serializer.data)
        else:
            return Response(status=status.HTTP_204_NO_CONTENT)


class DeleteVigilant(generics.DestroyAPIView):
    permissions = [IsAuthenticated, IsAdmin]

    queryset = Vigilante.objects.all()
    serializer_class = VigilanteSerializers
    lookup_field = 'pk'

    def delete(self, request, *args, **kwargs):
        instance = self.get_object()
        user = CustomUser.objects.get(id=instance.id_usuario.id)
        instance.delete()
        user.delete()
        return Response(status=status.HTTP_200_OK)




