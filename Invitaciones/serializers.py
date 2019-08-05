from rest_framework import serializers

from .models import *
from Usuarios.models import CustomUser
from Empresas.models import Administrador, Empresa, Area
from Empresas.models import Empleado


class json_invit_admin():
    """
    Object Class for render the input for the creation of
    invitations by Administrators.
    """
    def __init__(
            self,
            id_employee,
            cell_number,
            email,
            area,
            business,
            sec_equip,
            vehicle,
            company,
            notes,
            date):

        self.id_employee = id_employee
        self.cell_number = cell_number
        self.email = email
        self.id_area = area
        self.business = business
        self.sec_equip = sec_equip
        self.vehicle = vehicle
        self.company = company
        self.notes = notes
        self.date = date


class InvitationCreateSerializerAdmin(serializers.Serializer):
    """
    Serializer Class for create and validates Invitations created by an ADMIN
    """
    # employee_first_name = serializers.RegexField(regex=r'^[A-Za-z\s]+$', max_length=600)  # Not accept words with accent
    # employee_last_name = serializers.RegexField(regex=r'^[A-Za-z\s]+$', max_length=600)   # Not accept words with accent
    id_employee = serializers.IntegerField()
    cell_number = serializers.IntegerField(allow_null=True)
    email = serializers.EmailField(allow_blank=True)
    # area = serializers.CharField(max_length=100)
    area = serializers.IntegerField()
    business = serializers.CharField(max_length=300)
    sec_equip = serializers.CharField(max_length=300, allow_blank=True)
    vehicle = serializers.BooleanField()
    company = serializers.CharField(max_length=200)
    notes = serializers.CharField(max_length=300, allow_blank=True)
    date = serializers.DateTimeField(format='%Y-%m-%d %H:%M', input_formats=['%Y-%m-%d %H:%M'])

    def create(self, validated_data):
        return json_invit_admin(**validated_data)


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


class InvitationCreateSerializerEmployee(serializers.Serializer):
    """
    Serializer Class for creation of invitations by Employees.
    """
    cell_number = serializers.IntegerField()
    email = serializers.EmailField(allow_blank=True)
    # area = serializers.CharField(max_length=100)
    area = serializers.IntegerField()
    business = serializers.CharField(max_length=300)
    sec_equip = serializers.CharField(max_length=300, allow_blank=True)
    vehicle = serializers.BooleanField()
    company = serializers.CharField(max_length=200)
    notes = serializers.CharField(max_length=300, allow_blank=True)
    date = serializers.DateTimeField(format='%Y-%m-%d %H:%M', input_formats=['%Y-%m-%d %H:%M'])

    def create(self, validated_data):
        return json_invit_employee(**validated_data)


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
    #id_usuario = serializers.SerializerMethodField('get_user')


    class Meta:
        model = Invitacion  # Desired Model to be serialized.
        #fields = '__all__'  # Indicates that all fields in model should be used.
        fields = (
            'id_empresa',
            'id_area',
            'id_empleado',
            'id_usuario',
            'fecha_hora_envio',
            'fecha_hora_invitacion',
            'asunto',
            'automovil',
            'notas',
            'empresa',
            'leida'
        )

    def create(self, validated_data):
        print(validated_data)


class InvitationTmpSerializer(serializers.ModelSerializer):

    class Meta:
        model = InvitacionTemporal
        fields = '__all__'

class EquipoSeguridadSerializers(serializers.ModelSerializer):

    class Meta:
        model = EquipoSeguridad
        fields = '__all__'