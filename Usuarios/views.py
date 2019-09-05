from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from .serializers import *
from .permissions import *

from django.shortcuts import render

# Create your views here.


class UserPlatformCreateOrList(generics.CreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = UserPlatformSerializer


class UserUpdateParcial(generics.UpdateAPIView):
    permission_classes = [IsAuthenticated]

    def update(self, request, *args, **kwargs):
        instance = self.request.user
        # user = self.request.user

        print('prev mail =', instance.email)
        instance.email = request.data.get('email')
        print('post mail =', instance.email)
        instance.save()
        print(type(instance))


