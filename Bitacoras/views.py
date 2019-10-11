from rest_framework.response import Response
from rest_framework import generics, status, viewsets
from Usuarios.permissions import *
from .serializers import *
from Empresas.models import Vigilante, Administrador


class BitacoraListCreate(generics.ListCreateAPIView):
    permission_classes = (isEmployee | isGuard,)
    queryset = Bitacora.objects.all()
    serializer_class = BitacoraSerializers

    def create(self, request, *args, **kwargs):
        id_user = self.request.user.id
        vigilante = Vigilante.objects.filter(id_usuario=id_user)[0]
        print(vigilante.id_empresa.id)
        request.data['id_vigilante'] = vigilante.id
        request.data['id_empresa'] = vigilante.id_empresa.id
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class BitacoraUpdate(generics.UpdateAPIView):
    permission_classes = (isAdmin | isGuard, )
    queryset = Bitacora.objects.all()
    lookup_field = 'pk'
    serializer_class = BitacoraSerializers

    def partial_update(self, request, *args, **kwargs):
        kwargs['partial'] = True
        request.data['f_salida'] = datetime.now()
        return self.update(request, *args, **kwargs)


class BitacoraListGuard(viewsets.ModelViewSet):
    permission_classes = (isAdmin | isGuard, )
    serializer_class = BitacoraListGuardSerializers

    def list(self, request, *args, **kwargs):
        y = self.kwargs['year']
        m = self.kwargs['month']
        d = self.kwargs['day']
        usr = self.request.user
        registros = None
        if usr.roll == settings.ADMIN:  # Admin must be show all records of the Company.
            print('IS an ADMIN')
            admin_company = Administrador.objects.filter(id_usuario=usr)[0]
            id_company = admin_company.id_empresa
            registros = Bitacora.objects.filter(id_empresa=id_company, f_acceso__year=y,
                                                f_acceso__month=m,
                                                f_acceso__day=d)
        if usr.roll == settings.VIGILANTE:  # Guard must be show all records of the Company.
            print('IS an GUARD')
            guard_company = Vigilante.objects.filter(id_usuario=usr)[0]
            id_company = guard_company.id_empresa
            registros = Bitacora.objects.filter(id_empresa=id_company, f_acceso__year=y,
                                                f_acceso__month=m,
                                                f_acceso__day=d)

        queryset = self.queryset = registros
        serializer = BitacoraListGuardSerializers(queryset, many=True, context={"request": request})
        return Response(serializer.data)