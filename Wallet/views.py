from secrets import token_hex

from rest_framework.response import Response
from django.http import HttpResponse
from rest_framework.views import APIView
from django.conf import settings
from wallet.models import Pass, Barcode, EventTicket, BarcodeFormat, Location
from wsgiref.util import FileWrapper

from Invitaciones.models import InvitationByUsers


class GetWallet(APIView):

    def create_wallet(self, inv):
        event_info = EventTicket()
        event_info.addPrimaryField('hostName', f'{inv.host.first_name} {inv.host.last_name}', 'Anfitrión')
        event_info.addSecondaryField('dateTime', f'{inv.idInvitation.dateInv} - {inv.idInvitation.timeInv}', 'Fecha y Hora')
        event_info.addHeaderField('type', 'normal', 'Invitación')
        event_info.addAuxiliaryField('place', f'{inv.idInvitation.id_empresa.name}', 'Lugar')
        event_info.addBackField('subject', f'{inv.idInvitation.asunto}', 'Asunto')

        pass_file = Pass(
            event_info,
            passTypeIdentifier=settings.PASSTYPEIDENTIFIER,
            organizationName=settings.ORGANIZATIONNAME,
            teamIdentifier=settings.TEAMIDENTIFIER
        )

        pass_file.backgroundColor = 'rgb(227,237,255)'

        pass_file.serialNumber = token_hex(8)
        pass_file.barcode = Barcode(message=f'{inv.qr_code}', format=BarcodeFormat.QR, altText=f'{inv.qr_code}')
        pass_file.description = 'Invitación de Intrare'
        pass_file.voided = False

        with open(settings.MEDIA_ROOT + '/icon.png', mode='rb') as f:
            pass_file.addFile('icon.png', f)

        with open(settings.MEDIA_ROOT + '/thumbnail.png', mode='rb') as w:
            pass_file.addFile('logo.png', w)

        # with open(settings.MEDIA_ROOT + '/thumbnail.png', mode='rb') as t:
        #     pass_file.addFile('thumbnail.png', t)

        pass_file.create(
            settings.CRD + '/certificate.pem',
            settings.CRD + '/key.pem',
            settings.CRD + '/wwdr.pem',
            settings.WALLETPASS,
            settings.CRD + '/temp/test.pkpass'
        )

        try:
            file = open(settings.CRD + '/temp/test.pkpass', mode='rb')

            response = HttpResponse(FileWrapper(file), content_type='application/vnd.apple.pkpass')
            response['Pragma'] = 'no-cache'
            response['Cache-Control'] = 'no-store, no-cache, must-revalidate, post-check=0, pre-check=0'
            response['Content-Disposition'] = 'filename="pass.pkpass"'
            response['Content-Transfer-Encoding'] = 'binary'
            response.flush()

        except IOError:
            response = Response('Error interno: 00001')

        return response

    def get(self, request, qrcode):

        response = Response()
        invitacion = InvitationByUsers.objects.get(qr_code=qrcode)

        if invitacion:

            response = self.create_wallet(invitacion)
        else:
            response = Response('Error interno: 00002')

        return response



