# EndPoints


## **Usuarios**


### Eliminar un Token Device(Token de FireBase) de un determinado usuario en particular.

```
  -- request DELETE 
  -- url https://api-intrare-empresarial.herokuapp.com/User/Delete/Devices/
  -- header 'authorization: Token a405e2f1047905039d41800882d3afb162054ac1'
```  

### **Recuperacion de Contraseña**

  --request PATCH \
  --url http://127.0.0.1:8000/User/Reset/Passwordsita/ \
  --header 'content-type: application/json' \
  --data

  ```json
	{
	   "email":"aurelio.hdz.aguilar@gmail.com"
	}

```

### **Cargar la informacion de Un Usuario Por Token.**

**URL**: <urlHost>/getUser/**Token**/

**Descripcion:** Retornara la informacion necesaria para validar al nuevo usuario.


### **Eliminar un dispositivo de un Usuario**

**request** DELETE

**url** http://127.0.0.1:8000/User/Delete/Devices/

**header:** Token bd9ae482ea1a77239cd4cd89eb6159221cb03584'  El token debe de ser de alguien logueado


**json**
```json
{
	"idDevice":"CD2EEF2E-2BF7-4353-864F-2163A6C35303"
}
```


## **Invitaciones**

### Crear Invitacion Normal o Grupales

La unica diferencia entre una grupal o individual es el numero de valores en la clave guest.


**URL**: <urlHost>/create_inv/

**Descripcion:** Creara una invitacion tipo 0.

curl --request POST \
  --url http://127.0.0.1:8000/create_inv/ \
  --header 'authorization: Token 835a8271fd0c7a934c79e54c1310b2db890e12ce' \
  --header 'content-type: application/json' \
  --data

```json
{
	"areaId": 1,
	"secEquip":"",
	"guests":[
    {
      "email":"andes204@gmail.com",
      "cellphone":4443227734
    }],  
	"dateInv":"2019-09-30",
	"timeInv":"12:03",
	"exp":null,
	"subject":"nada en particular",
	"vehicle":false,
	"notes": "ninguna",
	"companyFrom": "daelabs",
	"employeeId":1,
	"diary":"",
  "typeInv":1
}
```

**Notas**
* typeInv: Tiene que ser 0 o 1 da igual para este tipo de invitacion.
* exp: null.
* dateInv: Se tiene que especificar una fecha

### Crear Recurrentes

Son invitaciones que pueden utilizarse ciertos dias de la semana, 
hasta una fecha de caducidad determinada.


**URL**: <urlHost>/create_inv/


curl --request POST \
  --url http://127.0.0.1:8000/create_inv/ \
  --header 'authorization: Token 835a8271fd0c7a934c79e54c1310b2db890e12ce' \
  --header 'content-type: application/json' \
  --data

```json
{
	"areaId": 1,
	"secEquip":"",
	"guests":[
    {
      "email":"andes204@gmail.com",
      "cellphone":4443227734
    }],  
	"dateInv":null,
	"timeInv":"12:03",
	"exp":"2019-09-30",
	"subject":"nada en particular",
	"vehicle":false,
	"notes": "ninguna",
	"companyFrom": "daelabs",
	"employeeId":1,
	"diary":"0136",
  "typeInv":2
}
```

**Notas**
* typeInv: Tiene que ser **2** para este tipo de invitacion.
* dateInv= null
* exp: Fecha de expiracion se tiene que especificar.

* diary: Es una cadena de longitud 7, en donde:
  - 0: Lunes.
  - 1: Martes.
  - 2: Miercoles
  - 3: Jueves.
  - 4: Viernes.
  - 5: Sabado.
  - 6: Domingo.



### Crear Invitaciones Empresariales parte 1.
Se usa cuando un anfitrion empieza el proceso de generacion de invitacion empresarial.

#### url 
http://127.0.0.1:8000/createReferredInv 
### header 
  **authorization**: Token 2877defe1623ff90d4c81eba66c4053f8222cd7c
#### JSON 
  ```json
  {
	"referredMail":"aurelio.hdz.aguilar@gmail.com",
	"host":2,
	"dateInv":"2019-10-14",
	"timeInv":"12:50",
	"vehicle":true,
	"subject":"Nada en particular",
	"idArea":1,
	"idCompany":1, 
	"companyFrom":"DaeLabs",
  "expiration":"2019-11-15",
  "type":0,
  "diary":""
}
```
#### Descripcion de ciertos Campos
- referredMail: Email del Referido, en este caso aquella persona que se designe como referido y que tenga 
  los permisos necesarios en la compañia, es decir tiene que tener los permisos de  administrador en la compañia invitada.
- host: Id del Anfritrion 
-expiration: Fecha de caducidad de la invitacion. Este campo puede o no ir, es decir require=False. 

**Aqui pueden ocurrir las mismas variantes Invitacion Normal o Invitacion Recurrente**


### Obtener una invitacion Empresarial 

**request GET**

**url** http://127.0.0.1:8000/getReferralInv/>TOKEN</

Obtiene una invitacion empresarial, referenciada por un TOKEN.

Retorna un JSON, como el siguiente:

```json
{
  "companyName": "Cordova Inc",
  "areaName": "Gerencia",
  "dateInv": "14-10-2019",
  "timeInv": "12:50",
  "hostFirstName": "Jessica",
  "hostLastName": "Jarvis",
  "subject": "Nada en particular",
  "dateSend": "15-10-2019"
}
```

### Concretar la creacion de la Invitacion Empresarial

***request** POST 

**url**  http://127.0.0.1:8000/createEnterpriseInv 

**header** 'authorization: Token a95e20dce4013b68c8949ea2fd39dccef40f60f7' \
 
 **JSON**
  ```json
  {
    "id_empresa": 1,
	  "guest":
    {
			"email":"andes204@gmail.com",
			"cellphone":4443227734
		},
    "areaId": 1,
    "dateInv": "2019-10-14",
    "timeInv": "12:50",
    "host": 2,
    "subject": "Nada en particular",
    "fecha_hora_envio": "2019-10-12",
    "expiration": "2019-10-16",
    "companyFrom": "DaeLabs",
    "diary": "",
	  "notes":"nada de nada", 
	  "idReferredInv":16
  }
```

***Descripcion de Campos**

- host : Id del Host(Anfitrion)
- idReferredInv: Es el ID de la invitacion Referida. Si se consume  http://127.0.0.1:8000/getReferralInv/>TOKEN</
  obtendra un json donde este viene contenido, y los campos necesarios para concretar la invitacion empresarial.


### Listar todas las invitacion que tiene un usuario, es decir en las que el Usuario es un INVITADO)

**Request:** GET

**url:** url http://127.0.0.1:8000/get_inv/user \

**header:** Authorization: Token cec70e2a2c6bc7102d2a3d603c03b897fb30020e   Token de un usuario logueado.

**Ejemplo JSON Que regresa**

```json
[
  {
    "id": 13,
    "typeInv": 0,
    "colorArea": "#5ef026",
    "companyName": "Rush-Parker",
    "areaName": "Gerencia",
    "hostFirstName": "Corey",
    "hostLastName": "Adams",
    "dateInv": "06-11-2019",
    "timeInv": "12:50",
    "asunto": "No quiero mi negro",
    "automovil": true,
    "qr_code": "73735335fec30d9912",
    "diary": "",
    "secEqu": [
      {
        "nameEquipment": "Guantes de Latex"
      },
      {
        "nameEquipment": "Casco de  Minero"
      }
    ]
  },
  {
    "id": 21,
    "typeInv": 0,
    "colorArea": "#5ef026",
    "companyName": "Rush-Parker",
    "areaName": "Gerencia",
    "hostFirstName": "Corey",
    "hostLastName": "Adams",
    "dateInv": "06-11-2019",
    "timeInv": "12:50",
    "asunto": "No quiero mi negro",
    "automovil": true,
    "qr_code": "76c2d9aa5b466a2512",
    "diary": "",
    "secEqu": [
      {
        "nameEquipment": "Guantes de Latex"
      },
      {
        "nameEquipment": "Casco de  Minero"
      }
    ]
  }
]
    "diary": "",
    "secEqu": [
      {
        "nameEquipment": "Guantes de Latex"
      },
      {
        "nameEquipment": "Casco de  Minero"
      }
    ]
  },
  {
    "id": 21,
    "typeInv": 0,
    "colorArea": "#5ef026",
    "companyName": "Rush-Parker",
    "areaName": "Gerencia",
    "hostFirstName": "Corey",
    "hostLastName": "Adams",
    "dateInv": "06-11-2019",
    "timeInv": "12:50",
    "asunto": "No quiero mi negro",
    "automovil": true,
    "qr_code": "76c2d9aa5b466a2512",
    "diary": "",
    "secEqu": [
      {
        "nameEquipment": "Guantes de Latex"
      },
      {
        "nameEquipment": "Casco de  Minero"
      }
    ]
  }
]
```

### Listar Invitaciones Realizadas por un Host, es decir las que ha realizado un Empleado o un Administrador


**url:**  http://127.0.0.1:8000/getInv/Admin/Employee/

**header:** Authorization: Token bd9ae482ea1a77239cd4cd89eb6159221cb03584'


**JSON** Que se retorna

```json
[
  {
    "id": 5,
    "typeInv": 2,
    "colorArea": "#a9e6f3",
    "companyName": "Oconnor, Jones and Snyder",
    "areaName": "Gerencia",
    "guestFirstName": "",
    "guestLastName": "",
    "dateInv": "30-10-2019",
    "timeInv": "22:03",
    "asunto": "nada en particular",
    "automovil": false,
    "qr_code": "4003a4702038dcd422",
    "diary": "0246",
    "secEqu": [
      {
        "nameEquipment": "Botas Antiderrapantes"
      },
      {
        "nameEquipment": "Lentes de Proteccion"
      },
      {
        "nameEquipment": "Guantes"
      }
    ],
    "expiration": "01-11-2019",
    "id_Invitation": 5
  },
  {
    "id": 13,
    "typeInv": 1,
    "colorArea": "#a9e6f3",
    "companyName": "Oconnor, Jones and Snyder",
    "areaName": "Gerencia",
    "guestFirstName": "",
    "guestLastName": "",
    "dateInv": "30-10-2019",
    "timeInv": "22:03",
    "asunto": "nada en particular",
    "automovil": false,
    "qr_code": "bc4ff639512fdf8722",
    "diary": "024",
    "secEqu": [
      {
        "nameEquipment": "Botas Antiderrapantes"
      },
      {
        "nameEquipment": "Lentes de Proteccion"
      },
      {
        "nameEquipment": "Guantes"
      }
    ],
    "expiration": "01-11-2019",
    "id_Invitation": 13
  }
]
```
### Eliminar Invitacion

**request**  DELETE

**url**  http://127.0.0.1:8000/deleteInvitation/>Id_Invitacion</

**header** 'authorization: Token bd9ae482ea1a77239cd4cd89eb6159221cb03584'  

Token debe de ser de un admin o un empleado. Obviamente el Id de la invitacion solmente lo va a tener el host que tiene acceso a sus propias invitaciones 

## Wallet
Solo cosuman GET /wallet/create/>qrCODE< 

regresa un pkpass.pkpass


## Empresa

### Dar de Alta Equipo de Seguridad 

Para esto es necesario, el Id del Area a la que se asignara este equipo de Seguridad, y el nombre del equipo de seguridad que desea dar de alta.


**Request:** POST

**url:** http://127.0.0.1:8000/addSecurityEquipment 

**header:** 'authorization: Token cfbced0fc65d1a3d2ba8044dc3035d146603c874' Este token tiene que ser de un administrador.

**JSON**

```json
{
	"nameEquipment": "Chaleco Seguridad",
	"idArea":2
}
```

### Actualizar Equipo de Seguridad

**request:** DELETE

**URL:** http://127.0.0.1:8000/deleteSecurityEquipment/>ID_EQUIPOSEGURIDAD</ 

**header:** 'authorization: Token cfbced0fc65d1a3d2ba8044dc3035d146603c874' Este token tiene que ser de un administrador.

**JSON**
```json
{
	"nameEquipment":"Guantes de Latex"
}
```


### Eliminar equipo de Seguridad

**request:** PATCH

**URL:** http://127.0.0.1:8000/updateSecurityEquipment/>ID_EQUIPOSEGURIDAD</ 

**header:** 'authorization: Token cfbced0fc65d1a3d2ba8044dc3035d146603c874' Este token tiene que ser de un administrador.


### Obtener Datos Invitacion por QR(GUARDIAS)
Obtiene el recurso con los datos relavantes para el guardia en el acceso.

La invitacion se obtiene a partir del su codigo(qrcode). 

**URL**
http://127.0.0.1:8000/get_inv/qr/>qrcode</

**JS0N**
```json
[
  {
    "id": 17,
    "areaName": "Gerencia",
    "areaColor": "#5ef026",
    "hostFirstName": "Corey",
    "hostLastName": "Adams",
    "host_ine_frente": null,
    "host_ine_atras": null,
    "host_celular": "7522141675",
    "guestFirstName": "",
    "guestLastName": "",
    "guest_ine_frente": null,
    "guest_ine_atras": null,
    "dateInv": "06-11-2019",
    "timeInv": "12:50",
    "asunto": "No quiero mi negro",
    "empresa": "Dildos el potosi",
    "automovil": true,
    "qr_code": "65087dc8c927d37412",
    "guestCellPhone": "4446354597",
    "notas": "No quiero mi negro",
    "logoEmpresa": "https://bucketeer-576c8228-7737-4878-8397-1c8403d07005.s3.amazonaws.com/PLC",
    "avatar": "https://bucketeer-576c8228-7737-4878-8397-1c8403d07005.s3.amazonaws.com/avatar.png",
    "secEqu": [
      {
        "nameEquipment": "Chaleco de Seguridad"
      },
      {
        "nameEquipment": "Casco de  Minero"
      }
    ]
  }
]
```


### Listar Equipo de Seguridad por Area

**REQUEST:** GET

**URL:** http://127.0.0.1:8000/get_SecurityEquipment/ByArea/>IDAREA</

**header:** authorization: Token bd9ae482ea1a77239cd4cd89eb6159221cb03584 El token pertenece a un administrador.

**JSON** que retorna

```json
[
  {
    "id": 4,
    "nameEquipment": "Lo que sea #1",
    "idArea": 2
  },
  {
    "id": 5,
    "nameEquipment": "Lo que sea #2",
    "idArea": 2
  }
]
```


### **Enviar Alerta** (Boton de Panico)

**request GET**

**url** http://127.0.0.1:8000/SendAlert

**header**  Authorization: Token bd5faeaaea1dc792721c228b309c333e6cd11d5f Token de un Administrador o un Empleado














