from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from django.core.exceptions import ObjectDoesNotExist
from Empresas.serializers import EmpresaSerializers

from .models import Providers
from Usuarios.models import CustomUser
from Usuarios.serializers import CustomFindSerializer
from Empresas.models import Empresa , Administrador

class ProvidersCompanySerializer(serializers.ModelSerializer):
    companyProvider = EmpresaSerializers(many=True)

    class Meta:
        model = Providers
        fields = '__all__'

class ProviderSerializer(serializers.ModelSerializer):

    # host = CustomFindSerializer()  # Esto hace mas lento el pedo

    class Meta:
        model = CustomUser
        fields = ['id','first_name', 'last_name', 'celular', 'host']


class UpdateProviderSerializer(serializers.ModelSerializer):
    celular = serializers.IntegerField(required=True, validators=[UniqueValidator(queryset=CustomUser.objects.all())])
    ine_frente = serializers.ImageField(required=True, allow_empty_file=False)
    ine_atras = serializers.ImageField(required=True, allow_empty_file=False)
    avatar = serializers.ImageField(required=True, allow_empty_file=False)

    class Meta:
        model = CustomUser
        fields = [
            'first_name',
            'last_name',
            'celular',
            'ine_frente',
            'ine_atras',
            'avatar'
        ]

    def update(self, instance, validated_data):
        instance.first_name = validated_data.pop('first_name')
        instance.last_name = validated_data.pop('last_name')
        instance.celular = validated_data.pop('celular')
        instance.ine_frente = validated_data.pop('ine_frente')
        instance.ine_atras = validated_data.pop('ine_atras')
        instance.avatar = validated_data.pop('avatar')
        instance.save()
        return instance



class FullProvider():
    def __init__(self,idUserAdminProvider, host, name, companyAddress, telephone, email, companyLogo,
                 companyWebPage, companyScian, companyClassification, companyLatitude, companyLongitude,
                 companyURLMap, companyValidity):
        self.idUserAdminProvider = idUserAdminProvider
        self.host = host
        self.name = name
        self.companyAddress = companyAddress
        self.telephone = telephone
        self.email = email
        self.companyLogo = companyLogo
        self.companyWebPage = companyWebPage
        self.companyScian = companyScian
        self.companyClassification = companyClassification
        self.companyLatitude = companyLatitude
        self.companyLongitude = companyLongitude
        self.companyURLMap = companyURLMap
        self.companyValidity = companyValidity

class CreateCompanyProviderSerializer(serializers.Serializer):
    idUserAdminProvider = serializers.IntegerField(required=True)
    host = serializers.IntegerField(required=True)
    name = serializers.CharField(required=True, validators=[UniqueValidator(queryset=Empresa.objects.all())])
    companyAddress = serializers.CharField(required=True)
    telephone = serializers.CharField(required=True, validators=[UniqueValidator(queryset=Empresa.objects.all())])
    email = serializers.EmailField(required=True, validators=[UniqueValidator(queryset=Empresa.objects.all())])
    companyLogo =  serializers.ImageField(required=True)
    companyWebPage = serializers.CharField(required=True)
    companyScian = serializers.IntegerField(required=True)
    companyClassification = serializers.CharField(required=True)
    companyLatitude = serializers.FloatField(required=True)
    companyLongitude = serializers.FloatField(required=True)
    companyURLMap = serializers.CharField(required=True)
    companyValidity = serializers.DateField(required=True)


    def create(self, validated_data):
        return FullProvider(**validated_data)

        # Actualizar Token Proveedor(borrarlo)
        # Crear Empresa
        # Crear admin de la empresa con datos proveedor
        # Crear registro provedor con host - proveedor
        # Notifcar al Host que ha sido exitosa la alta.






