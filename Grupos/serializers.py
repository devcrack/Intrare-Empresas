from rest_framework import serializers
from .models import *
from Usuarios.models import CustomUser


class GrupoSerializers(serializers.ModelSerializer):
    class Meta:
        model = Grupo
        fields = '__all__'


class ContactosXGrupoSerializers(serializers.ModelSerializer):
    nombre_usuario = serializers.CharField(source='id_contacto.first_name')
    apellido_usuario = serializers.CharField(source='id_contacto.last_name')
    celular_usuario = serializers.CharField(source='id_contacto.celular')
    email_usuario = serializers.CharField(source='id_contacto.email')
    avatar_usuario = serializers.CharField(source='id_contacto.avatar')

    class Meta:
        model = Grupo_has_contacto
        fields = ('id',
                  'id_grupo',
                  'id_contacto',
                  'nombre_usuario',
                  'apellido_usuario',
                  'celular_usuario',
                  'email_usuario',
                  'avatar_usuario',
                  )


class ContactosXGrupoSerializersCreate(serializers.ModelSerializer):
    class Meta:
        model = Grupo_has_contacto
        fields = '__all__'

