from rest_framework import serializers

from .models import Providers
from Usuarios.models import CustomUser
from Usuarios.serializers import CustomFindSerializer

class GetProviderSerializer(serializers.ModelSerializer):

    host = CustomFindSerializer(many=True)

    class Meta:
        model = CustomUser
        fields = ['first_name', 'last_name', 'celular', 'host']
