from djoser.serializers import UserSerializer as BaseUserSerializer


class UserSerializer(BaseUserSerializer):
    class Meta(BaseUserSerializer.Meta):
        fields = ('email', 'username', 'roll', 'first_name', 'last_name', 'celular', 'is_staff', 'is_superuser')