from rest_framework import serializers
from .models import *


class ContactoSerializers(serializers.ModelSerializer):
    class Meta:
        model = Contacto
        fields = '__all__'

