from django.utils import regex_helper
from rest_framework import serializers
from .models import *
from Usuarios.models import CustomUser
from django.core.exceptions import ObjectDoesNotExist
from django.template.loader import render_to_string
from ControlAccs.utils import send_IntrareEmail


from Empresas.models import Administrador, Empresa, Area
from Empresas.models import Empleado, SecurityEquipment


linkInvitationData = "https://web-intrare.herokuapp.com/form_invitation_data/"  # Link Development
# linkInvitationData = "https://first-project-vuejs.herokuapp.com/form_invitation_data/"  # Link Production V1

_date = date(year=timezone.datetime.now().year, month=timezone.datetime.now().month,
             day=timezone.datetime.now().day)  # Fecha actual


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

# class EquipoSeguridadSerializers(serializers.ModelSerializer):
#     class Meta:
#         model = EquipoSeguridad
#         fields = '__all__'
#
#
# class EquipoSeguridadXInvitacionSerializers(serializers.ModelSerializer):
#     name_equipamnet = serializers.CharField(source='id_equipo_seguridad.nombre')
#
#     class Meta:
#         model = EquiposporInvitacion
#         fields = ('name_equipamnet',)


class SecurityEquipmentSerializer(serializers.ModelSerializer):

    class Meta:
        model = SecurityEquipment
        fields = ['nameEquipment']


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
    secEqu = serializers.SerializerMethodField('getSecEqu')
    diary = serializers.CharField(source='idInvitation.diary')
    expiration = serializers.DateField(source='idInvitation.expiration', format="%d-%m-%Y")

    class Meta:
        model = InvitationByUsers
        fields = ('id', 'typeInv', 'colorArea', 'companyName', 'areaName', 'hostFirstName', 'hostLastName', 'dateInv',
                  'timeInv', 'asunto', 'automovil', 'qr_code', 'diary', 'secEqu', 'expiration', 'confirmed')

    def getSecEqu(self, obj):
        _areaId = obj.idInvitation.id_area
        _securityEquipment = SecurityEquipment.objects.filter(idArea=_areaId)
        _serializerData = SecurityEquipmentSerializer(data=_securityEquipment, many=True)
        _serializerData.is_valid()
        return _serializerData.data


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
    diary = serializers.CharField(source='idInvitation.diary')
    secEqu = serializers.SerializerMethodField('getSecEqu')
    expiration = serializers.DateField(source='idInvitation.expiration', format="%d-%m-%Y")
    id_Invitation = serializers.IntegerField(source='idInvitation.id')

    class Meta:
        model = InvitationByUsers
        fields = ('id', 'typeInv', 'colorArea', 'companyName', 'areaName', 'guestFirstName', 'guestLastName', 'dateInv',
                  'timeInv', 'asunto', 'automovil', 'qr_code', 'diary', 'secEqu', 'expiration','id_Invitation',
                  'confirmed')

    def getSecEqu(self, obj):
        _areaId = obj.idInvitation.id_area
        _securityEquipment = SecurityEquipment.objects.filter(idArea=_areaId)
        _serializerData = SecurityEquipmentSerializer(data=_securityEquipment, many=True)
        _serializerData.is_valid()
        return _serializerData.data



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
    notas = serializers.CharField(source='idInvitation.notas')
    secEqu = serializers.SerializerMethodField('getSecEqu')
    expiration = serializers.DateField(source='idInvitation.expiration', format="%d-%m-%Y")
    # Mamadas del Andres
    typeInv = serializers.IntegerField(source='idInvitation.typeInv')
    diary = serializers.CharField(source='idInvitation.diary')
    id_Invitation = serializers.IntegerField(source='idInvitation.id')

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
            'avatar',
            'secEqu',
            'expiration',
            # Mamadas del Andres
            'typeInv',
            'diary',
            'id_Invitation',
            'confirmed'
        )

    def getSecEqu(self, obj):
        _areaId = obj.idInvitation.id_area
        _securityEquipment = SecurityEquipment.objects.filter(idArea=_areaId)
        _serializerData = SecurityEquipmentSerializer(data=_securityEquipment, many=True)
        _serializerData.is_valid()
        return _serializerData.data

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
    def __init__(self, areaId, guests, subject, typeInv, dateInv, timeInv, exp, diary,
                 companyFrom, notes, vehicle):
        self.areaId = areaId #
        self.guests = guests #
        self.subject = subject #
        self.typeInv = typeInv #
        self.dateInv = dateInv #
        self.timeInv = timeInv #
        self.exp = exp #
        self.diary = diary #
        self. companyFrom = companyFrom #
        self.notes = notes #
        self.vehicle = vehicle


class MasiveInvSerializer(serializers.Serializer):
    areaId = serializers.IntegerField()
    guests = BasicDataUserSerializer(many=True)
    subject = serializers.CharField(max_length=400)  #
    typeInv = serializers.IntegerField(default=0)  #
    dateInv = serializers.DateField(format="%Y-%m-%d", input_formats=["%Y-%m-%d"], allow_null=True)
    timeInv = serializers.TimeField(format="%H:%M", input_formats=['%H:%M'])  #
    exp = serializers.DateField(format="%Y-%m-%d", input_formats=["%Y-%m-%d"], allow_null=True)  #
    diary = serializers.CharField(max_length=7, allow_blank=True)
    vehicle = serializers.BooleanField(default=False)
    companyFrom = serializers.CharField(max_length=200, allow_blank=True, allow_null=True)
    notes = serializers.CharField(max_length=300, allow_blank=True, allow_null=True)

    def create(self, validated_data):
        return MassiveInvObject(**validated_data)

    def validate(self, data):
        if data['dateInv'] != None:
            if _date > data['dateInv']:
                raise serializers.ValidationError("La fecha de la invitacion esta vencida")
        if data['exp'] != None:
            if data['exp'] < _date:
                raise serializers.ValidationError("La fecha de expiracion no puede ser en una fecha "
                                                  "Vencida")
        return data


class ReferredInvitationSerializerCreate(serializers.ModelSerializer):
    referredMail = serializers.EmailField(allow_null=False)
    referredPhone = serializers.RegexField(regex=r'^(\d{10})(?:\s|$)', max_length=10, allow_null=True, required=False)
    # qrCode = serializers.CharField(required=False, max_length=100)
    dateInv = serializers.DateField(format="%Y-%m-%d", input_formats=["%Y-%m-%d"])
    host = serializers.IntegerField(required=False)
    timeInv = serializers.TimeField(format="%H:%M", input_formats=['%H:%M'])
    notes = serializers.CharField(default="", max_length=300, allow_blank=True)
    exp = serializers.DateField(format="%Y-%m-%d", input_formats=["%Y-%m-%d"], required=False)
    Token = serializers.CharField(required=False)

    class Meta:
        model = ReferredInvitation
        fields = '__all__'

    def validate(self, data):
        if _date > data['dateInv']:
            raise serializers.ValidationError("La fecha de la invitacion esta vencida "
                                              "acontezca la invitacion")

        _referredMail = data['referredMail'] # Guest
        usr = self.context['request'].user #Host
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
        _fromCompany = _adminGuest.id_empresa.name
        if _fromCompany != data['companyFrom']:
            raise serializers.ValidationError("La empresa del referido No es la Correcta. Favor de Corregir")
        return data

    def create(self, validated_data):

        usr = self.context['request'].user
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
        _token = token_hex(7)
        _nwReferredInv = ReferredInvitation(id_empresa=_companyID, areaId=validated_data['areaId'],
                                            dateInv=validated_data['dateInv'], timeInv=validated_data['timeInv'],
                                            subject=validated_data['subject'], vehicle=validated_data['vehicle'],
                                            notes=validated_data['notes'], companyFrom=validated_data['companyFrom'],
                                            host=usr, referredMail=_referredMail, Token=_token)
        _nwReferredInv.save()
        _link = linkInvitationData + _nwReferredInv.Token
        html_message = render_to_string("referredMail.html",
                                        {
                                            "link": _link
                                        })
        send_IntrareEmail(html_message, _referredMail)
        return _nwReferredInv


class GetReferralInvSerializer(serializers.ModelSerializer):
    companyName = serializers.CharField(source='id_empresa.name')
    areaName = serializers.CharField(source='areaId.nombre')
    dateInv = serializers.DateField(format="%d-%m-%Y")
    timeInv = serializers.TimeField(format="%H:%M")
    hostFirstName = serializers.CharField(source='host.first_name')
    hostLastName = serializers.CharField(source='host.last_name')
    # fecha_hora_envio = serializers.DateTimeField(format="%d-%m-%Y")

    class Meta:
        model = ReferredInvitation
        fields = ['id', 'id_empresa', 'companyName', 'areaId', 'areaName', 'dateInv', 'timeInv', 'host', 'hostFirstName',
                  'hostLastName', 'subject', 'fecha_hora_envio', 'expiration', 'companyFrom', 'diary']



class EnterpriseInvObject():
    def __init__(self, areaId, fecha_hora_envio, dateInv, timeInv, expiration, diary,
                 companyFrom, notes, vehicle, subject, id_empresa, host, guest, idReferredInv):
        self.areaId = areaId #
        self.fecha_hora_envio = fecha_hora_envio
        self.dateInv = dateInv
        self.timeInv = timeInv
        self.expiration = expiration
        self.diary = diary
        self.subject = subject  #
        self.vehicle = vehicle
        self.guest = guest
        self.companyFrom = companyFrom  #
        self.notes = notes
        self.id_empresa = id_empresa
        self.host = host
        self.idReferredInv = idReferredInv


class EnterpriseSerializer(serializers.Serializer):
    areaId = serializers.IntegerField()
    guest = BasicDataUserSerializer()
    fecha_hora_envio = serializers.DateTimeField(format="%Y-%m-%d", input_formats=["%Y-%m-%d"])
    dateInv = serializers.DateField(format="%Y-%m-%d", input_formats=["%Y-%m-%d"])
    timeInv = serializers.TimeField(format="%H:%M")
    expiration = serializers.DateField(format="%Y-%m-%d", input_formats=["%Y-%m-%d"])
    diary = serializers.CharField(max_length=7, allow_blank=True)
    subject = serializers.CharField(max_length=400)
    vehicle = serializers.BooleanField(default=False)
    companyFrom = serializers.CharField(max_length=200, allow_blank=True, allow_null=True)
    notes = serializers.CharField(max_length=300, allow_blank=True, allow_null=True)
    host = serializers.IntegerField()
    id_empresa = serializers.IntegerField()
    idReferredInv = serializers.IntegerField()


    def create(self, validated_data):

        return EnterpriseInvObject(**validated_data)


class FullInvitationSerializer(serializers.ModelSerializer):

    class Meta:
        model = Invitacion
        fields = '__all__'


class InvitationByUsersSerializer(serializers.ModelSerializer):

    class Meta:
        model = InvitationByUsers
        fields = '__all__'






