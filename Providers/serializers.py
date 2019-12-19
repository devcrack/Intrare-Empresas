from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from .models import Providers
from Usuarios.models import CustomUser
from Usuarios.serializers import CustomFindSerializer

class ProviderSerializer(serializers.ModelSerializer):

    # host = CustomFindSerializer()  # Esto hace mas lento el pedo

    class Meta:
        model = CustomUser
        fields = ['first_name', 'last_name', 'celular', 'host']


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


