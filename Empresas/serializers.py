from rest_framework import serializers
from .models import *


class EmpresaSerializers(serializers.ModelSerializer):
    class Meta:
        model = Empresa
        fields = '__all__'


class AdministradorSerializers(serializers.ModelSerializer):
    class Meta:
        model = Administrador
        fields = '__all__'


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



