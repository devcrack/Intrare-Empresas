from djoser.serializers import UserSerializer as BaseUserSerializer
from rest_framework import serializers
from django.contrib.auth.validators import UnicodeUsernameValidator
from rest_framework.exceptions import ValidationError
from django.utils import translation

from .models import *


class UserSerializer(BaseUserSerializer):
    class Meta(BaseUserSerializer.Meta):
        fields = ('email', 'username', 'roll', 'first_name', 'last_name', 'celular', 'is_staff', 'is_superuser')


class UserAdminSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = '__all__'
        extra_kwargs = {
            'celular': {
                'validators': []
            },
            'email': {
                'validators': []
            },
            'username': {
                'validators': []
            }
        }

    def validate_celular(self, value):
        check_query = CustomUser.objects.filter(celular=value)
        if self.instance:
            check_query = check_query.exclude(pk=self.instance.id_usuario.pk)

        if self.parent is not None and self.parent.instance is not None:
            celular = getattr(self.parent.instance, self.field_name)
            check_query = check_query.exclude(pk=celular.pk)

        if check_query.exists():
            if translation.get_language() == 'es':
                raise serializers.ValidationError('Ya existe un celular con ese número.')
            if translation.get_language() == 'en':
                raise serializers.ValidationError('There is already a cell phone with that number.')
        return value

    def validate_email(self, value):
        check_query = CustomUser.objects.filter(email=value)
        if self.instance:
            check_query = check_query.exclude(pk=self.instance.id_usuario.pk)

        if self.parent is not None and self.parent.instance is not None:
            email = getattr(self.parent.instance, self.field_name)
            check_query = check_query.exclude(pk=email.pk)

        if check_query.exists():
            if translation.get_language() == 'es':
                raise serializers.ValidationError('Ya existe un usuario con ese E-Mail.')
            if translation.get_language() == 'en':
                raise serializers.ValidationError('A user with that E-Mail already exists.')
        return value


    def validate_username(self, value):
        check_query = CustomUser.objects.filter(username=value)
        if self.instance:
            check_query = check_query.exclude(pk=self.instance.id_usuario.pk)

        if self.parent is not None and self.parent.instance is not None:
            username = getattr(self.parent.instance, self.field_name)
            check_query = check_query.exclude(pk=username.pk)

        if check_query.exists():
            if translation.get_language() == 'es':
                raise serializers.ValidationError('Ya existe un usuario con ese Nombre de Usuario.')
            if translation.get_language() == 'en':
                raise serializers.ValidationError('A user with that User Name already exists.')
        return value


class UserEmployeeSerializer(serializers.ModelSerializer):

    class Meta:
        model = CustomUser
        fields = (
            'first_name',
            'last_name',
            'email',
            'is_active',
            'celular',
            'roll',
            'ine_frente',
            'ine_atras',
            'groups',
            'user_permissions',
            'password'
        )
        extra_kwargs = {
            'celular': {
                'validators': []
            },
            'email': {
                'validators': []
            },
            'username': {
                'validators': []
            },
            'password': {'write_only': True}
        }

    def __init__(self, *args, **kwargs):
        self.fields['first_name'] = serializers.CharField(required=True, allow_null=False, allow_blank=False)
        self.fields['last_name'] = serializers.CharField(required=True, allow_null=False, allow_blank=False)
        self.fields['username'] = serializers.CharField(required=False, allow_null=False, allow_blank=False)
        self.fields['password'] = serializers.CharField(required=False, allow_null=True, allow_blank=True)
        self.fields['email'] = serializers.EmailField(required=True, allow_null=False, allow_blank=False)
        return super(UserEmployeeSerializer, self).__init__(*args, **kwargs)

    def validate_celular(self, value):
        check_query = CustomUser.objects.filter(celular=value)
        if self.instance:
            check_query = check_query.exclude(pk=self.instance.id_usuario.pk)

        if self.parent is not None and self.parent.instance is not None:
            celular = getattr(self.parent.instance, self.field_name)
            check_query = check_query.exclude(pk=celular.pk)

        if check_query.exists():
            if translation.get_language() == 'es':
                raise serializers.ValidationError('Ya existe un celular con ese número.')
            if translation.get_language() == 'en':
                raise serializers.ValidationError('There is already a cell phone with that number.')
        return value

    def validate_email(self, value):
        check_query = CustomUser.objects.filter(email=value)
        if self.instance:
            check_query = check_query.exclude(pk=self.instance.id_usuario.pk)

        if self.parent is not None and self.parent.instance is not None:
            email = getattr(self.parent.instance, self.field_name)
            check_query = check_query.exclude(pk=email.pk)

        if check_query.exists():
            if translation.get_language() == 'es':
                raise serializers.ValidationError('Ya existe un usuario con ese E-Mail.')
            if translation.get_language() == 'en':
                raise serializers.ValidationError('A user with that E-Mail already exists.')
        return value


    def validate_username(self, value):
        check_query = CustomUser.objects.filter(username=value)
        if self.instance:
            check_query = check_query.exclude(pk=self.instance.id_usuario.pk)

        if self.parent is not None and self.parent.instance is not None:
            username = getattr(self.parent.instance, self.field_name)
            check_query = check_query.exclude(pk=username.pk)

        if check_query.exists():
            if translation.get_language() == 'es':
                raise serializers.ValidationError('Ya existe un usuario con ese Nombre de Usuario.')
            if translation.get_language() == 'en':
                raise serializers.ValidationError('A user with that User Name already exists.')
        return value


class UserVigilanteSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = '__all__'
        extra_kwargs = {
            'celular': {
                'validators': []
            },
            'email': {
                'validators': []
            },
            'username': {
                'validators': []
            }
        }

    def __init__(self, *args, **kwargs):
        self.fields['first_name'] = serializers.CharField(required=True, allow_null=False, allow_blank=False)
        self.fields['last_name'] = serializers.CharField(required=True, allow_null=False, allow_blank=False)
        self.fields['username'] = serializers.CharField(required=False, allow_null=False, allow_blank=False)
        self.fields['password'] = serializers.CharField(required=False, allow_null=True, allow_blank=True)
        self.fields['email'] = serializers.EmailField(required=True, allow_null=False, allow_blank=False)
        self.fields['celular'] = serializers.CharField(max_length=30, allow_null=False, allow_blank=False)
        return super(UserVigilanteSerializer, self).__init__(*args, **kwargs)

    def validate_celular(self, value):
        check_query = CustomUser.objects.filter(celular=value)
        if self.instance:
            check_query = check_query.exclude(pk=self.instance.id_usuario.pk)

        if self.parent is not None and self.parent.instance is not None:
            celular = getattr(self.parent.instance, self.field_name)
            check_query = check_query.exclude(pk=celular.pk)

        if check_query.exists():
            if translation.get_language() == 'es':
                raise serializers.ValidationError('Ya existe un celular con ese número.')
            if translation.get_language() == 'en':
                raise serializers.ValidationError('There is already a cell phone with that number.')
        return value

    def validate_email(self, value):
        check_query = CustomUser.objects.filter(email=value)
        if self.instance:
            check_query = check_query.exclude(pk=self.instance.id_usuario.pk)

        if self.parent is not None and self.parent.instance is not None:
            email = getattr(self.parent.instance, self.field_name)
            check_query = check_query.exclude(pk=email.pk)

        if check_query.exists():
            if translation.get_language() == 'es':
                raise serializers.ValidationError('Ya existe un usuario con ese E-Mail.')
            if translation.get_language() == 'en':
                raise serializers.ValidationError('A user with that E-Mail already exists.')
        return value


    def validate_username(self, value):
        check_query = CustomUser.objects.filter(username=value)
        if self.instance:
            check_query = check_query.exclude(pk=self.instance.id_usuario.pk)

        if self.parent is not None and self.parent.instance is not None:
            username = getattr(self.parent.instance, self.field_name)
            check_query = check_query.exclude(pk=username.pk)

        if check_query.exists():
            if translation.get_language() == 'es':
                raise serializers.ValidationError('Ya existe un usuario con ese Nombre de Usuario.')
            if translation.get_language() == 'en':
                raise serializers.ValidationError('A user with that User Name already exists.')
        return value


class UserPlatformSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = (
            'password',
            'username',
            'first_name',
            'last_name',
            'email',
            'celular',
            'ine_frente',
            'ine_atras',
        )


































