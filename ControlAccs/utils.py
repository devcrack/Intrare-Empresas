# Servicio de SMS Nexmo
import nexmo
from django.core.mail import send_mail
from django.conf import settings

CLIENT = nexmo.Client(key='532e50a4', secret='7Rh1PbAbDRApW2jw')
subject = 'Intrare Industrial - Invitación'
email_from = settings.EMAIL_HOST_USER

def send_sms(number, message):
    """

    :param number: Numero Celular del Destinatario
    :param message: Contenido del mensaje, valga la redundancia
    :return: Respuesta de la transaccion al enviar el sms.
    """
    strNumber = str(number)
    lenStr = len(strNumber)
    if lenStr > 10:
        to_number = strNumber
    else:
        to_number = '52' + strNumber

    responseData = CLIENT.send_message(
        {
            "from": "Intrare Empresarial",
            "to": to_number,
            "text": message,
            }
        )
    return responseData

def send_IntrareEmail(html_message, email):
    recipient_list = [email, ]
    _subject = 'Intrare Industrial'
    msg = ''
    send_mail(subject=_subject, from_email=email_from, message= msg, recipient_list=recipient_list,
              html_message=html_message)
