from djoser.serializers import UserSerializer as BaseUserSerializer
from rest_framework import serializers
from django.contrib.auth.validators import UnicodeUsernameValidator
from rest_framework.exceptions import ValidationError
from djoser.serializers import UserCreateSerializer as BaseUserRegistrationSerializer

from django.utils import translation

from .models import *
from django.contrib.auth import validators


class UserSerializer(BaseUserSerializer):
    class Meta(BaseUserSerializer.Meta):
        fields = ('id', 'email', 'username', 'roll', 'first_name', 'last_name', 'celular', 'is_staff', 'is_superuser', 'avatar', 'temporalToken')


class CustomUserSerializer(serializers.ModelSerializer):
    first_name = serializers.CharField(required=True, allow_null=False, allow_blank=False)
    last_name = serializers.CharField(required=True, allow_null=False, allow_blank=False)
    email = serializers.EmailField(allow_blank=False)
    ine_frente = serializers.ImageField(required=True, allow_empty_file=False)

    class Meta:
        model = CustomUser
        fields = [
            'first_name',
            'last_name',
            'email',
            'username',
            'celular',
            'ine_frente',
            'temporalToken',
            'password'
        ]



class CustomFindSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['email', 'first_name', 'last_name', 'celular', 'avatar']


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

    def __init__(self, *args, **kwargs):
        self.fields['first_name'] = serializers.CharField(required=True, allow_null=False, allow_blank=False)
        self.fields['last_name'] = serializers.CharField(required=True, allow_null=False, allow_blank=False)
        self.fields['username'] = serializers.CharField(required=False, allow_null=False, allow_blank=False)
        self.fields['password'] = serializers.CharField(required=False, allow_null=True, allow_blank=True)
        self.fields['email'] = serializers.EmailField(required=True, allow_null=False, allow_blank=False)
        self.fields['celular'] = serializers.CharField(max_length=30, allow_null=False, allow_blank=False)
        return super(UserAdminSerializer, self).__init__(*args, **kwargs)

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


class UserPlatformSerializer(BaseUserRegistrationSerializer):
    class Meta(BaseUserRegistrationSerializer.Meta):
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


class validatorImg():

    def __init__(self, imgFront, imgBack):
        self.imgFront = imgFront
        self.imgBack = imgBack

class UpdateIneSerializser(serializers.Serializer):
    imgFront = serializers.ImageField(allow_null=False,  allow_empty_file=False)
    imgBack = serializers.ImageField(allow_null=False, allow_empty_file=False)

    def create(self, validated_data):
        return validatorImg(**validated_data)

class validatorONEImg():

    def __init__(self, img):
        self.img = img

class UpdateOneIMGSerializser(serializers.Serializer):
    img = serializers.ImageField(allow_null=False,  allow_empty_file=False)

    def create(self, validated_data):
        return validatorONEImg(**validated_data)


class validatorUserUpdate():

    def __init__(self, email, username, first_name, last_name):
        self.email = email
        self.username = username
        self.first_name = first_name
        self.last_name = last_name

class UpdateUserByTempToken(serializers.Serializer):
    username_validator = UnicodeUsernameValidator()

    email = serializers.EmailField()
    username = serializers.CharField(
        max_length=150,
        help_text=('Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.'),
        validators = [username_validator])
































