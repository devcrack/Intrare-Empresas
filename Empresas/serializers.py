from rest_framework import serializers
from .models import *
from Usuarios.serializers import UserAdminSerializer, UserEmployeeSerializer, UserVigilanteSerializer
from Usuarios.models import CustomUser
from Invitaciones.models import Invitacion

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
        if id_usuario_data['password'] != '':
            usuario.set_password(id_usuario_data['password'])
        usuario.is_active = id_usuario_data['is_active']
        usuario.save()
        instance.id_usuario.username = id_usuario_data['username']
        instance.id_usuario.first_name = id_usuario_data['first_name']
        instance.id_usuario.last_name = id_usuario_data['last_name']
        instance.id_usuario.email = id_usuario_data['email']
        instance.id_usuario.celular = id_usuario_data['celular']
        instance.id_usuario.password = usuario.password
        instance.id_empresa = validated_data['id_empresa']
        instance.id_usuario.is_active = id_usuario_data['is_active']
        instance.save()
        return instance


class AreaSerializers(serializers.ModelSerializer):
    class Meta:
        model = Area
        fields = '__all__'


class VigilanteSerializers(serializers.ModelSerializer):
    id_usuario = UserVigilanteSerializer(many=False)

    class Meta:
        model = Vigilante
        fields = '__all__'

    def create(self, validated_data):
        id_usuario_data = validated_data.pop('id_usuario')
        usuario = CustomUser.objects.create(**id_usuario_data)
        usuario.set_password(id_usuario_data['password'])
        usuario.save()
        vigilante = Vigilante.objects.create(id_usuario=usuario, **validated_data)
        return vigilante

    def update(self, instance, validated_data):
        id_usuario_data = validated_data.pop('id_usuario')
        usuario = CustomUser.objects.get(pk=instance.id_usuario.id)
        usuario.username = id_usuario_data['username']
        usuario.first_name = id_usuario_data['first_name']
        usuario.last_name = id_usuario_data['last_name']
        usuario.email = id_usuario_data['email']
        usuario.celular = id_usuario_data['celular']
        if id_usuario_data['password'] != '':
            usuario.set_password(id_usuario_data['password'])
        usuario.is_active = id_usuario_data['is_active']
        usuario.save()
        instance.id_usuario.username = id_usuario_data['username']
        instance.id_usuario.first_name = id_usuario_data['first_name']
        instance.id_usuario.last_name = id_usuario_data['last_name']
        instance.id_usuario.email = id_usuario_data['email']
        instance.id_usuario.celular = id_usuario_data['celular']
        instance.id_usuario.password = usuario.password
        instance.id_empresa = validated_data['id_empresa']
        instance.id_usuario.is_active = id_usuario_data['is_active']
        instance.save()
        return instance


class EmpleadoSerializers(serializers.ModelSerializer):
    id_usuario = UserEmployeeSerializer(many=False)

    class Meta:
        model = Empleado
        fields = '__all__'

    def create(self, validated_data):
        id_usario_data = validated_data.pop('id_usuario')
        id_usario_data.pop('groups')
        id_usario_data.pop('user_permissions')
        usuario = CustomUser.objects.create(**id_usario_data)
        usuario.set_password(id_usario_data['password'])
        usuario.save()
        employee = Empleado.objects.create(id_usuario=usuario, **validated_data)
        return employee

    def update(self, instance, validated_data):
        id_usuario_data = validated_data.pop('id_usuario')
        usuario = CustomUser.objects.get(pk=instance.id_usuario.id)
        usuario.username = id_usuario_data['username']
        usuario.first_name = id_usuario_data['first_name']
        usuario.last_name = id_usuario_data['last_name']
        usuario.email = id_usuario_data['email']
        usuario.celular = id_usuario_data['celular']
        usuario.ine_frente = id_usuario_data['ine_frente']
        usuario.ine_atras = id_usuario_data['ine_atras']
        if id_usuario_data['password'] != '':
            usuario.set_password(id_usuario_data['password'])
        usuario.is_active = id_usuario_data['is_active']
        usuario.save()
        instance.id_usuario.username = id_usuario_data['username']
        instance.id_usuario.first_name = id_usuario_data['first_name']
        instance.id_usuario.last_name = id_usuario_data['last_name']
        instance.id_usuario.email = id_usuario_data['email']
        instance.id_usuario.celular = id_usuario_data['celular']
        instance.id_usuario.ine_frente = id_usuario_data['ine_frente']
        instance.id_usuario.ine_atras = id_usuario_data['ine_atras']
        instance.id_usuario.is_active = id_usuario_data['is_active']
        instance.id_usuario.password = usuario.password
        instance.extension = validated_data['extension']
        instance.puede_enviar = validated_data['puede_enviar']
        instance.id_notificaciones = validated_data['id_notificaciones']
        instance.codigo = validated_data['codigo']
        instance.id_empresa = validated_data['id_empresa']
        instance.id_area = validated_data['id_area']
        instance.save()
        return instance

class CasetaSerializers(serializers.ModelSerializer):
    class Meta:
        model = Caseta
        fields = '__all__'


class AccesUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Acceso

class AccessSerializer(serializers.ModelSerializer):
    class Meta:
        model = Acceso
        fields = '__all__'
class jsonAcceso():
    def __init__(self, datos_coche, qr_code):
        self.datos_coche = datos_coche
        self.qr_code = qr_code


class AccessCreateSerializer(serializers.Serializer):
    datos_coche = serializers.CharField(max_length=300, allow_blank=True, allow_null=True)
    qr_code = serializers.CharField(max_length=16)


    def create(self, validated_data):
        return jsonAcceso(**validated_data)


class AccessDetail(serializers.ModelSerializer):
    guestFName = serializers.CharField(source='id_invitacion.id_usuario.first_name')
    guestLName = serializers.CharField(source='id_invitacion.id_usuario.last_name')
    companyName = serializers.CharField(source='id_invitacion.empresa')
    hostFirstName = serializers.CharField(source='id_invitacion.id_empleado.id_usuario.first_name')
    hostLastName = serializers.CharField(source='id_invitacion.id_empleado.id_usuario.last_name')
    fecha_hora_acceso = serializers.DateTimeField(format="%d/%m/%Y %H:%M")
    fecha_hora_salida = serializers.DateTimeField(format="%d/%m/%Y %H:%M")

    class Meta:
        model = Acceso
        fields = ('id', 'guestFName', 'guestLName', 'companyName', 'fecha_hora_acceso', 'fecha_hora_salida', 'hostFirstName',
                  'hostLastName')