from rest_framework import serializers
from .models import *


class ContactoSerializers(serializers.ModelSerializer):
    class Meta:
        model = Contacto
        fields = '__all__'


class GrupoSerializers(serializers.ModelSerializer):
    class Meta:
        model = Grupo
        fields = '__all__'


class ContactosXGrupoSerializers(serializers.ModelSerializer):
    nombreContacto = serializers.CharField(source='id_contacto.nombre')
    celularContacto = serializers.CharField(source='id_contacto.telefono')

    class Meta:
        model = Grupo_has_contacto
        fields = ('id', 'id_grupo', 'id_contacto', 'nombreContacto', 'celularContacto')


class ContactosXGrupoSerializersCreate(serializers.ModelSerializer):
    class Meta:
        model = Grupo_has_contacto
        fields = '__all__'

