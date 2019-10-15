from django.utils import regex_helper
from rest_framework import serializers
from .models import *
from Usuarios.models import CustomUser
from django.core.exceptions import ObjectDoesNotExist
from django.template.loader import render_to_string
from ControlAccs.utils import send_IntrareEmail, send_sms


from Empresas.models import Administrador, Empresa, Area
from Empresas.models import Empleado


class InvitacionSerializers(serializers.ModelSerializer):
    """ Serializer just for invitations.

    Class Evidently extended from ModelSerializer.
    The ModelSerializer class provides a shortcut that lets you automatically create a Serializer class
    with fields that correspond to the Model fields.

    The ModelSerializer class is the same as a regular Serializer class, except that:
    It will automatically generate a set of fields for you, based on the model.
    It will automatically generate validators for the serializer, such as unique_together validators.
    It includes simple default implementations of .create() and .update().
    """
    class Meta:
        model = Invitacion  # Desired Model to be serialized.
        #fields = '__all__'  # Indicates that all fields in model should be used.
        fields = (
            'id_empresa',
            'id_area',
            'id_empleado',
            'id_usuario',
            'fecha_hora_envio',
            'dateInv',
            'timeInv',
            'asunto',
            'automovil',
            'notas',
            'empresa',
            'leida'
        )

class EquipoSeguridadSerializers(serializers.ModelSerializer):
    class Meta:
        model = EquipoSeguridad
        fields = '__all__'


class EquipoSeguridadXInvitacionSerializers(serializers.ModelSerializer):
    name_equipamnet = serializers.CharField(source='id_equipo_seguridad.nombre')

    class Meta:
        model = EquiposporInvitacion
        fields = ('name_equipamnet',)


class InvitationToSimpleUserSerializer(serializers.ModelSerializer):
    companyName = serializers.CharField(source='idInvitation.id_empresa.name')
    areaName = serializers.CharField(source='idInvitation.id_area.nombre')
    hostFirstName = serializers.CharField(source='host.first_name')
    hostLastName = serializers.CharField(source='host.last_name')
    dateInv = serializers.DateField(source='idInvitation.dateInv',format="%d-%m-%Y")  # Nuevo
    timeInv = serializers.TimeField(source='idInvitation.timeInv',format="%H:%M")  # Nuevo
    colorArea = serializers.CharField(source='idInvitation.id_area.color')
    typeInv = serializers.IntegerField(source='idInvitation.typeInv')
    asunto = serializers.CharField(source='idInvitation.asunto')
    automovil = serializers.BooleanField(source='idInvitation.automovil')
    # qr_code = serializers.CharField(source='idInvitation.qr_code')
    diary = serializers.CharField(source='idInvitation.diary')

    class Meta:
        model = InvitationByUsers
        fields = ('id', 'typeInv', 'colorArea', 'companyName', 'areaName', 'hostFirstName', 'hostLastName', 'dateInv', 'timeInv',
                  'asunto', 'automovil', 'qr_code', 'diary')


class InvitationToHostSerializer(serializers.ModelSerializer):
    companyName = serializers.CharField(source='idInvitation.id_empresa.name')
    areaName = serializers.CharField(source='idInvitation.id_area.nombre')
    guestFirstName = serializers.CharField(source='idGuest.first_name')
    guestLastName = serializers.CharField(source='idGuest.last_name')
    dateInv = serializers.DateField(source='idInvitation.dateInv',format="%d-%m-%Y")  # Nuevo
    timeInv = serializers.TimeField(source='idInvitation.timeInv',format="%H:%M")  # Nuevo
    colorArea = serializers.CharField(source='idInvitation.id_area.color')
    typeInv = serializers.IntegerField(source='idInvitation.typeInv')
    asunto = serializers.CharField(source='idInvitation.asunto')
    automovil = serializers.BooleanField(source='idInvitation.automovil')
    # qr_code = serializers.CharField(source='idInvitation.qr_code')
    diary = serializers.CharField(source='idInvitation.diary')

    class Meta:
        model = InvitationByUsers
        fields = ('id', 'typeInv', 'colorArea', 'companyName', 'areaName', 'guestFirstName', 'guestLastName', 'dateInv',
                  'timeInv', 'asunto', 'automovil', 'qr_code', 'diary')


class InvitationToGuardSerializer(serializers.ModelSerializer):
    """
    Para listar la invitacion al guardia en el acceso
    """
    areaName = serializers.CharField(source='idInvitation.id_area.nombre')
    areaColor = serializers.CharField(source='idInvitation.id_area.color')
    hostFirstName = serializers.CharField(source='host.first_name')
    hostLastName = serializers.CharField(source='host.last_name')
    host_ine_frente = serializers.ImageField(source='host.ine_frente')
    host_ine_atras = serializers.ImageField(source='host.ine_atras')
    host_celular = serializers.CharField(source='host.celular')
    guestFirstName = serializers.CharField(source='idGuest.first_name')
    guestLastName = serializers.CharField(source='idGuest.last_name')
    guest_ine_frente = serializers.ImageField(source='idGuest.ine_frente')
    guest_ine_atras = serializers.ImageField(source='idGuest.ine_atras')
    guestCellPhone = serializers.CharField(source='idGuest.celular')
    avatar = serializers.ImageField(source='idGuest.avatar')
    dateInv = serializers.DateField(source='idInvitation.dateInv', format="%d-%m-%Y")  # Nuevo
    timeInv = serializers.TimeField(source='idInvitation.timeInv', format="%H:%M")  # Nuevo
    logoEmpresa = serializers.ImageField(source='idInvitation.id_empresa.logo')
    asunto = serializers.CharField(source='idInvitation.asunto')
    empresa = serializers.CharField(source='idInvitation.empresa')
    automovil = serializers.BooleanField(source='idInvitation.automovil')
    # qr_code = serializers.CharField(source='idInvitation.qr_code')
    notas = serializers.CharField(source='idInvitation.notas')

    class Meta:
        model = InvitationByUsers
        fields = (
            'id',
            'areaName',
            'areaColor',
            'hostFirstName',
            'hostLastName',
            'host_ine_frente',
            'host_ine_atras',
            'host_celular',
            'guestFirstName',
            'guestLastName',
            'guest_ine_frente',
            'guest_ine_atras',
            'dateInv',
            'timeInv',
            'asunto',
            'empresa',
            'automovil',
            'qr_code',
            'guestCellPhone',
            'notas',
            'logoEmpresa',
            'avatar'
        )


class BasicUserObject():
    def __init__(self, email, cellphone):
        self.email = email
        self.cellphone = cellphone


class BasicDataUserSerializer(serializers.Serializer):
    email = serializers.EmailField(allow_null=True)
    cellphone = serializers.IntegerField()

    def create(self, validated_data):
        return BasicUserObject(**validated_data)

class MassiveInvObject():
    def __init__(self, areaId, guests, subject, typeInv, dateInv, timeInv, exp, diary, secEquip,
                 companyFrom, notes, vehicle):
        self.areaId = areaId #
        self.guests = guests #
        self.subject = subject #
        self.typeInv = typeInv #
        self.dateInv = dateInv #
        self.timeInv = timeInv #
        self.exp = exp #
        self.diary = diary #
        self.secEquip = secEquip #
        self. companyFrom = companyFrom #
        self.notes = notes #
        self.vehicle = vehicle

class MasiveInvSerializer(serializers.Serializer):
    areaId = serializers.IntegerField()
    guests = BasicDataUserSerializer(many=True)
    subject = serializers.CharField(max_length=400)  #
    typeInv = serializers.IntegerField(default=0)  #
    dateInv = serializers.DateField(format="%Y-%m-%d", input_formats=["%Y-%m-%d"])
    timeInv = serializers.TimeField(format="%H:%M", input_formats=['%H:%M'])  #
    exp = serializers.DateField(format="%Y-%m-%d", input_formats=["%Y-%m-%d"], allow_null=True)  #
    diary = serializers.CharField(max_length=7, allow_blank=True)
    secEquip = serializers.RegexField(regex=r'^[0-9,]+$', max_length=25, allow_null=True, allow_blank=True)
    vehicle = serializers.BooleanField(default=False)
    companyFrom = serializers.CharField(max_length=200, allow_blank=True, allow_null=True)
    notes = serializers.CharField(max_length=300, allow_blank=True, allow_null=True)

    def create(self, validated_data):
        return MassiveInvObject(**validated_data)

    def validate(self, data):
        # Validando la fecha de la invitacion
        _date = date(year=timezone.datetime.now().year, month=timezone.datetime.now().month,
                     day=timezone.datetime.now().day)  # Fecha actual
        if _date > data['dateInv']:
            raise serializers.ValidationError("La fecha de la invitacion esta vencida")
        # Validando que la fecha de expiracion sea mayor o igual a la fecha de la invitacion.
        if data['exp'] != None:
            if data['exp'] < data['dateInv']:
                raise serializers.ValidationError("La fecha de expiracion no puede ser antes de que "
                                                  "acontezca la invitacion")
        return data


# def get_Company(idUsr):
#     try:
#         _host = CustomUser.objects.get(id=idUsr)
#     except ObjectDoesNotExist:
#         return None
#     try:
#         admin = Administrador.objects.get(id_usuario=_host)
#     except ObjectDoesNotExist:
#         return None
#     return admin.id_empresa


class ReferredInvitationSerializerCreate(serializers.ModelSerializer):
    referredMail = serializers.EmailField(allow_null=False)
    referredPhone = serializers.RegexField(regex=r'^(\d{10})(?:\s|$)', max_length=10, allow_null=True, required=False)
    # qrCode = serializers.CharField(required=False, max_length=100)
    dateInv = serializers.DateField(format="%Y-%m-%d", input_formats=["%Y-%m-%d"])
    # host = serializers.IntegerField()
    timeInv = serializers.TimeField(format="%H:%M", input_formats=['%H:%M'])
    notes = serializers.CharField(default="")
    expiration = serializers.DateField(format="%Y-%m-%d", input_formats=["%Y-%m-%d"], required=False)

    class Meta:
        model = ReferredInvitation
        fields = '__all__'

    def validate(self, data):
        _referredMail = data['referredMail']
        usr = data['host']
        try:
            guest = CustomUser.objects.get(email=_referredMail)
        except ObjectDoesNotExist:
            raise serializers.ValidationError("El referido no es un Usuario de Intrare")
        try:
            _adminGuest = Administrador.objects.get(id_usuario=guest)
        except ObjectDoesNotExist:
            raise serializers.ValidationError("El referido no cumple con los permisos necesarios")
        if usr.roll == settings.ADMIN:
            try:
                _admCompany = Administrador.objects.get(id_usuario=usr)
            except ObjectDoesNotExist:
                return None
            _companyID = _admCompany.id_empresa
        else:
            try:
                _employee = Empleado.objects.get(id_usuario=usr)
            except ObjectDoesNotExist:
                return None
            _companyID = _employee.id_empresa
        _companyGuest = _adminGuest.id_empresa
        if _companyID == _companyGuest:
            raise serializers.ValidationError("¿Quieres delegar tus obligaciones a alguien mas?")
        return data

    def create(self, validated_data):
        usr = validated_data['host']
        _referredMail = validated_data['referredMail']
        if usr.roll == settings.ADMIN:
            try:
                _admCompany = Administrador.objects.get(id_usuario=usr)
            except ObjectDoesNotExist:
                return None
            _companyID = _admCompany.id_empresa
        else:
            try:
                _employee = Empleado.objects.get(id_usuario=usr)
            except ObjectDoesNotExist:
                return None
            _companyID = _employee.id_empresa
        _nwReferredInv = ReferredInvitation(idCompany=_companyID, idArea=validated_data['idArea'],
                                            dateInv=validated_data['dateInv'], timeInv=validated_data['timeInv'],
                                            subject=validated_data['subject'], vehicle=validated_data['vehicle'],
                                            notes=validated_data['notes'], companyFrom=validated_data['companyFrom'],
                                            host=usr, referredMail=_referredMail)
        _nwReferredInv.save()
        _link = "URL/" + _nwReferredInv.Token
        html_message = render_to_string("referredMail.html",
                                        {
                                            "link": _link
                                        })
        send_IntrareEmail(html_message, _referredMail)
        return _nwReferredInv

class GetReferralInvSerializer(serializers.ModelSerializer):
    companyName = serializers.CharField(source='idCompany.name')
    areaName = serializers.CharField(source='idArea.nombre')
    dateInv = serializers.DateField(format="%d-%m-%Y")
    timeInv = serializers.TimeField(format="%H:%M")
    hostFirstName = serializers.CharField(source='host.first_name')
    hostLastName = serializers.CharField(source='host.last_name')
    dateSend = serializers.DateTimeField(format="%d-%m-%Y")

    class Meta:
        model = ReferredInvitation
        fields = ['companyName', 'areaName', 'dateInv', 'timeInv', 'hostFirstName', 'hostLastName', 'subject',
                  'dateSend']






