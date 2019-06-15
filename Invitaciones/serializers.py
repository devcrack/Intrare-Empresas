from rest_framework import serializers

from .models import *
from Empresas.models import Administrador,Empresa
from Empresas.models import Empleado


class InvitacionCreateSerializer(serializers.Serializer):
    # cell_number = serializers.IntegerField()
    # email = serializers.EmailField()
    # area = serializers.CharField()
    # inv_date = serializers.DateField()
    # business = serializers.CharField()
    # sec_equip = serializers.CharField()
    # vehicle = serializers.BooleanField()
    # notes = serializers.CharField()
    # company_from = serializers.CharField()
    email = serializers.EmailField()
    content = serializers.CharField(max_length=200)
    created = serializers.DateTimeField()

    def create(self, validated_data):
        print('HELLO FROM INVITATION_CREATE_SERIALIZER fuckeeeeerr!!!!!\n')











































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

    # def is_valid(self, raise_exception=False):1
    #     print('INITIAL DATA\n')
    #     print(self.initial_data)
    #     print('HELLO from IS VALID Method\n')
    #     return True


class InvitationTmpSerializer(serializers.ModelSerializer):

    class Meta:
        model = InvitacionTemporal
        fields = '__all__'

