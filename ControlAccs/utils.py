# Servicio de SMS Nexmo
import nexmo
from django.core.mail import send_mail
from django.conf import settings
import random


CLIENTNEXMO = nexmo.Client(key='e61cdd65', secret='eNn7ZmzMIQjQ3Kpr')
subject = 'Intrare Empresas - Invitación'
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
    print('Enviando SMS a ' + to_number +'\n')
    responseData = CLIENTNEXMO.send_message(
        {
            "from": "Intrare Empresas",
            "to": to_number,
            "text": message,
            }
        )
    print('Saldo NEXMO\n')
    print(CLIENTNEXMO.get_balance())
    return responseData

def send_IntrareEmail(html_message, email):
    print("Enviando Mail a " + email)
    recipient_list = [email, ]
    _subject = 'Intrare Industrial'
    msg = ''
    send_mail(subject=_subject, from_email=email_from, message= msg, recipient_list=recipient_list,
              html_message=html_message)

def phn():
    n = '0000000000'
    while '9' in n[3:6] or n[3:6]=='000' or n[6]==n[7]==n[8]==n[9]:
        n = str(random.randint(10**9, 10**10-1))
    return n[:3] + n[3:6] + n[6:]