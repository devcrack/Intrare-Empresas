from rest_framework import serializers
from .models import *
from Usuarios.serializers import UserAdminSerializer
from Usuarios.models import CustomUser

class EmpresaSerializers(serializers.ModelSerializer):
    class Meta:
        model = Empresa
        fields = '__all__'


class AdministradorSerializers(serializers.ModelSerializer):
    id_usuario = UserAdminSerializer(many=False)

    class Meta:
        model = Administrador
        fields = '__all__'

    def create(self, validated_data):
        id_usuario_data = validated_data.pop('id_usuario')
        usuario = CustomUser.objects.create(**id_usuario_data)
        admon = Administrador.objects.create(id_usuario=usuario, **validated_data)
        return admon

class AreaSerializers(serializers.ModelSerializer):
    class Meta:
        model = Area
        fields = '__all__'


class VigilanteSerializers(serializers.ModelSerializer):
    class Meta:
        model = Vigilante
        fields = '__all__'


class EmpleadoSerializers(serializers.ModelSerializer):
    class Meta:
        model = Empleado
        fields = '__all__'


class CasetaSerializers(serializers.ModelSerializer):
    class Meta:
        model = Caseta
        fields = '__all__'
