from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from django.core.exceptions import ObjectDoesNotExist


from .models import Providers
from Usuarios.models import CustomUser
from Usuarios.serializers import CustomFindSerializer
from Empresas.models import Empresa

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


class CreateCompanyProviderSerializer(serializers.Serializer):
    idAdminProvider = serializers.IntegerField(required=True)
    host = serializers.IntegerField(required=True)
    companyName = serializers.CharField(required=True)
    companyAddress = serializers.CharField(required=True)
    companyTelephone = serializers.CharField(required=True)
    companyEmail = serializers.EmailField(required=True)
    companyLogo =  serializers.ImageField(required=True)
    companyWebPage = serializers.CharField(required=True)
    companyScian = serializers.IntegerField(required=True)
    companyClassification = serializers.CharField(required=True)
    companyLatitude = serializers.FloatField(required=True)
    companyLongitude = serializers.FloatField(required=True)
    companyURLMap = serializers.CharField(required=True)
    companyValidity = serializers.DateField(required=True)


    def create(self, validated_data):
        pass
        # _idProvider = validated_data['idAdminProvider']
        # _idHost = validated_data['idAdminProvider']
        # try:
        #     usrProvider = CustomUser.objects.get(id=_idProvider)
        #     usrHost = CustomUser.objects.get(id=_idHost)
        # except ObjectDoesNotExist:
        #     return None
        # nameCompany = validated_data['companyName']
        # companyAddress = validated_data['companyAddress']
        #
        #
        # nwCompany = Empresa(name=
        #
        # )
        # Actualizar Token Proveedor(borrarlo)
        # Crear Empresa
        # Crear admin de la empresa con datos proveedor
        # Crear registro provedor con host - proveedor
        # Notifcar al Host que ha sido exitosa la alta.






