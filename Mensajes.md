# SMS
## Validacion de Usuario Nuevo
"Hola Anfitrion, valida a tu Invitado para que empieze a usar Intrare."
## Invitacion Nueva
"Se te ha enviado una invitacion, verifica desde tu correo electronico o en la aplicacion"
## Invitado ha llegado 
"Tu invitado " + _guestFullName + " proveniente de: " + _from+  " ha llegado"
Donde:
    - _guestFullName : Nombre completo del invitado
    -  _from = Empresa de donde viene 
## Firmar pase de salida a invitado para que pueda salir 
"Firma el pase de salida del Invitado: " + _guestFullName + "\nFecha y Hora de Acceso:" + _dateTimeAcc
Donde:
    - _guestFulllName : Nombre completo del invitado
    - _dateTimeAcc: Hora del acceso del invitado al recinto.

 
## Invitacion nueva a usuario NO registrado

"Intrare.Recibisite una Invitacion por favor realiza tu peregitros en " + LINK

Donde:
- URL unica para que el usuario nuevo realize su preregistro.