from rest_framework.response import Response
from django.http import HttpResponse, HttpResponseNotFound
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from django.conf import settings as set
import os
from wallet.models import Pass, Barcode, EventTicket, BarcodeFormat
from wsgiref.util import FileWrapper

class GetWallet(APIView):
    # permission_classes = [IsAuthenticated]


    def get(self, request, format=None):
        json = request.data

        eventInfo = EventTicket()
        eventInfo.addPrimaryField('test', 'text', 'test')


        passFile = Pass(
            eventInfo,
            passTypeIdentifier=set.PASSTYPEIDENTIFIER,
            organizationName=set.ORGANIZATIONNAME,
            teamIdentifier=set.TEAMIDENTIFIER
        )

        passFile.serialNumber = '184568974563224457'
        passFile.barcode = Barcode(message='test tets', format=BarcodeFormat.QR)
        passFile.relevantDate = "2019-11-28T12:00:00Z"
        passFile.description = 'accesos intrare'
        passFile.voided = False

        with open(set.MEDIA_ROOT+'/icon.png', mode='rb') as f:
            passFile.addFile('icon.png', f)

        with open(set.MEDIA_ROOT+'/logo.png', mode='rb') as w:
            passFile.addFile('logo.png', w)


        passFinal = passFile.create(
            set.CRD+'/certificate.pem',
            set.CRD+'/key.pem',
            set.CRD+'/wwdr.pem',
            set.WALLETPASS,
            set.CRD+'/temp/test.pkpass'
        )

        try:
            file = open(set.CRD+'/temp/test.pkpass', mode='rb')

            response = HttpResponse(FileWrapper(file), content_type='application/vnd.apple.pkpass')
            response['Pragma'] = 'no-cache'
            response['Cache-Control'] = 'no-store, no-cache, must-revalidate, post-check=0, pre-check=0'
            response['Content-Disposition'] = 'filename="pass.pkpass"'
            #response['Content-Length'] = str(os.stat(set.CRD+'/temp/test.pkpass').st_size)
            response['Content-Transfer-Encoding'] = 'binary'
            response.flush()
            #response.data = file.read()


        except IOError:
            response = Response('Error')

        return response
