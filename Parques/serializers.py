from rest_framework import serializers
from .models import *



class ParqueSerializers(serializers.ModelSerializer):
    class Meta:
        model = Parque
        fields = '__all__'
