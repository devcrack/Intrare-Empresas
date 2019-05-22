from rest_framework import serializers
from .models import Empresa
from Parques.models import Parque
from Usuarios.models import CustomUser


class EmpresaSerializers(serializers.ModelSerializer):
    class Meta:
        model = Empresa
        fields = '__all__'


