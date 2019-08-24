from rest_framework import generics

from .serializers import *
from .permissions import *
from django.shortcuts import render

# Create your views here.


class UserPlatformCreateOrList(generics.CreateAPIView):
    permission_classes = (isSuperAdmin | isEmployee,)
    queryset = CustomUser.objects.all()
    serializer_class = UserPlatformSerializer
