from djoser.serializers import UserSerializer as BaseUserSerializer
from rest_framework import serializers
from .models import *


class UserSerializer(BaseUserSerializer):
    class Meta(BaseUserSerializer.Meta):
        fields = ('email', 'username', 'roll', 'first_name', 'last_name', 'celular', 'is_staff', 'is_superuser')


class UserAdminSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = '__all__'


class UserEmployeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = '__all__'