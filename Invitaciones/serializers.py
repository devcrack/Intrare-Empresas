from django.utils import regex_helper
from rest_framework import serializers
from .models import *
from Usuarios.models import CustomUser
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

class json_invit_admin():
    """
    Object Class for render the input for the creation of
    invitations by Administrators.
    """

    def __init__(self, areaId, employeeId, cellNumber, email, subject, typeInv, dateInv, timeInv, exp, diary,
                 secEquip, vehicle, companyFrom, notes,
                 ):
        self.areaId = areaId
        self.employeeId = employeeId
        self.cellNumber = cellNumber
        self.email = email
        self.subject = subject
        self.typeInv = typeInv
        self.dateInv = dateInv
        self.timeInv = timeInv
        self.exp = exp
        self.diary = diary
        self.secEquip = secEquip
        self.vehicle = vehicle
        self.companyFrom = companyFrom
        self.notes = notes


class InvitationCreateSerializerAdmin(serializers.Serializer):
    """
    Serializer Class for create and validates Invitations created by an ADMIN
    """
    areaId = serializers.IntegerField()  #
    employeeId = serializers.IntegerField(allow_null=True)  #
    cellNumber = serializers.IntegerField(allow_null=True)  #
    email = serializers.EmailField(allow_null=True, allow_blank=False)  #
    subject = serializers.CharField(max_length=400)  #
    typeInv = serializers.IntegerField(default=0)  #
    dateInv = serializers.DateField(format="%Y-%m-%d", input_formats=["%Y-%m-%d"])
    timeInv = serializers.TimeField(format="%H:%M", input_formats=['%H:%M'])  #
    exp = serializers.DateField(format="%Y-%m-%d", input_formats=["%Y-%m-%d"], allow_null=True)  #
    diary = serializers.CharField(max_length=7, allow_blank=True)
    secEquip = serializers.RegexField(regex=r'^[0-9,]+$', max_length=25, allow_null=True, allow_blank=True)
    vehicle = serializers.BooleanField()
    companyFrom = serializers.CharField(max_length=200, allow_blank=True, allow_null=True)
    notes = serializers.CharField(max_length=300, allow_blank=True, allow_null=True)

    def create(self, validated_data):
        return json_invit_admin(**validated_data)

    def validate(self, data):
        # Validando la fecha de la invitacion
        _date = date(year=timezone.datetime.now().year, month=timezone.datetime.now().month,
                     day=timezone.datetime.now().day)  # Fecha actual
        if _date > data['dateInv']:
            raise serializers.ValidationError("La fecha de la invitacion esta vencida")
        # Validando que se haya ingresado el email o el numero de telefono, pero no ninguno de los 2.
        if data['cellNumber'] == None and data['email'] == None:
            raise serializers.ValidationError("Tienes que ingresar email o numero de Telefono")
        # Validando que la fecha de expiracion sea mayor o igual a la fecha de la invitacion.
        if data['exp'] != None:
            if data['exp'] < data['dateInv']:
                raise serializers.ValidationError(
                    "La fecha de expiracion no puede ser antes de que acontezca la invitacion")
        return data


class json_invit_employee():
    """
    Object Class for render the json input data for create invitations by
    employees.
    """

    def __init__(self, cell_number, email, area, business, sec_equip, vehicle, company, notes, date):
        self.cell_number = cell_number
        self.email = email
        self.area = area
        self.business = business
        self.sec_equip = sec_equip
        self.vehicle = vehicle
        self.company = company
        self.notes = notes
        self.date = date


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
    companyName = serializers.CharField(source='id_empresa.name')
    areaName = serializers.CharField(source='id_area.nombre')
    hostFirstName = serializers.CharField(source='id_empleado.id_usuario.first_name')
    hostLastName = serializers.CharField(source='id_empleado.id_usuario.last_name')
    dateInv = serializers.DateField(format="%d-%m-%Y")  # Nuevo
    timeInv = serializers.TimeField(format="%H:%M")  # Nuevo
    expiration = serializers.DateField(format="%d-%m-%Y")  # Nuevo

    class Meta:
        model = Invitacion
        fields = ('companyName', 'areaName', 'hostFirstName', 'hostLastName', 'dateInv', 'timeInv', 'expiration',
                  'asunto', 'automovil', 'qr_code')


class InvitationToGuardSerializer(serializers.ModelSerializer):
    """
    Para listar la invitacion al guardia en el acceso
    """
    areaName = serializers.CharField(source='id_area.nombre')
    areaColor = serializers.CharField(source='id_area.color')
    hostFirstName = serializers.CharField(source='id_empleado.id_usuario.first_name')
    hostLastName = serializers.CharField(source='id_empleado.id_usuario.last_name')
    host_ine_frente = serializers.ImageField(source='id_empleado.id_usuario.ine_frente')
    host_ine_atras = serializers.ImageField(source='id_empleado.id_usuario.ine_atras')
    host_celular = serializers.CharField(source='id_empleado.id_usuario.celular')
    extension = serializers.CharField(source='id_empleado.extension')
    guestFirstName = serializers.CharField(source='id_usuario.first_name')
    guestLastName = serializers.CharField(source='id_usuario.last_name')
    guest_ine_frente = serializers.ImageField(source='id_usuario.ine_frente')
    guest_ine_atras = serializers.ImageField(source='id_usuario.ine_atras')
    guestCellPhone = serializers.CharField(source='id_usuario.celular')
    dateInv = serializers.DateField(format="%d-%m-%Y")  # Nuevo
    timeInv = serializers.TimeField(format="%H:%M")  # Nuevo
    expiration = serializers.DateField(format="%d-%m-%Y")  # Nuevo
    logoEmpresa = serializers.CharField(source='id_empleado.id_empresa.logo')

    class Meta:
        model = Invitacion
        fields = (
            'id',
            'areaName',
            'areaColor',
            'hostFirstName',
            'hostLastName',
            'host_ine_frente',
            'host_ine_atras',
            'host_celular',
            'extension',
            'guestFirstName',
            'guestLastName',
            'guest_ine_frente',
            'guest_ine_atras',
            'dateInv',
            'timeInv',
            'expiration',
            'asunto',
            'empresa',
            'automovil',
            'qr_code',
            'guestCellPhone',
            'notas',
            'logoEmpresa'
        )


class InvitationSimpleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Invitacion
        fields = '__all__'
