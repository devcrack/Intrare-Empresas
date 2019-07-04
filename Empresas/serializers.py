from rest_framework import serializers
from .models import *
from Usuarios.serializers import UserAdminSerializer, UserEmployeeSerializer
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
        usuario.set_password(id_usuario_data['password'])
        usuario.save()
        admon = Administrador.objects.create(id_usuario=usuario, **validated_data)
        return admon

    def update(self, instance, validated_data):
        id_usuario_data = validated_data.pop('id_usuario')
        usuario = CustomUser.objects.get(pk=instance.id_usuario.id)
        usuario.username = id_usuario_data['username']
        usuario.first_name = id_usuario_data['first_name']
        usuario.last_name = id_usuario_data['last_name']
        usuario.email = id_usuario_data['email']
        usuario.celular = id_usuario_data['celular']
        usuario.set_password(id_usuario_data['password'])
        usuario.save()
        instance.id_usuario.username = id_usuario_data['username']
        instance.id_usuario.first_name = id_usuario_data['first_name']
        instance.id_usuario.last_name = id_usuario_data['last_name']
        instance.id_usuario.email = id_usuario_data['email']
        instance.id_usuario.celular = id_usuario_data['celular']
        instance.id_usuario.password = id_usuario_data['password']
        instance.id_empresa = validated_data['id_empresa']
        instance.save()
        return instance




class AreaSerializers(serializers.ModelSerializer):
    class Meta:
        model = Area
        fields = '__all__'


class VigilanteSerializers(serializers.ModelSerializer):
    class Meta:
        model = Vigilante
        fields = '__all__'


class EmpleadoSerializers(serializers.ModelSerializer):
    id_usuario = UserEmployeeSerializer(many=False)

    class Meta:
        model = Empleado
        fields = '__all__'

    def create(self, validated_data):
        id_usario_data = validated_data.pop('id_usuario')
        usuario = CustomUser.objects.create(**id_usario_data)
        usuario.set_password(id_usario_data['password'])
        usuario.save()
        employee = Empleado.objects.create(id_usuario=usuario, **validated_data)
        return employee

class CasetaSerializers(serializers.ModelSerializer):
    class Meta:
        model = Caseta
        fields = '__all__'
