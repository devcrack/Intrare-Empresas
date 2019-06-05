from rest_framework import serializers

from .models import *
from Empresas.models import Administrador,Empresa
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
        fields = '__all__'  # Indicates that all fields in model should be used.

        
