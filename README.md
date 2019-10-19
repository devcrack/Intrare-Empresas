# EndPoints


## **Usuarios**


### Eliminar un Token Device(Token de FireBase) de un determinado usuario en particular.

```
  -- request DELETE 
  -- url https://api-intrare-empresarial.herokuapp.com/User/Delete/Devices/
  -- header 'authorization: Token a405e2f1047905039d41800882d3afb162054ac1'
```  

### Recuperacion de Contraseña

  --request PATCH \
  --url http://127.0.0.1:8000/User/Reset/Passwordsita/ \
  --header 'content-type: application/json' \
  --data

  ```json
	{
	   "email":"aurelio.hdz.aguilar@gmail.com"
	}

```

### Cargar la informacion de Un Usuario Por Token.

**URL**: <urlHost>/getUser/**Token**/

**Descripcion:** Retornara la informacion necesaria para validar al nuevo usuario.


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
	"diary":""
}

```
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
  "expiration":"2019-11-15"
}
```
#### Descripcion de ciertos Campos
- referredMail: Email del Referido, en este caso aquella persona que se designe como referido y que tenga 
  los permisos necesarios en la compañia, es decir tiene que tener los permisos de  administrador en la compañia invitada.
- host: Id del Anfritrion 
-expiration: Fecha de caducidad de la invitacion. Este campo puede o no ir, es decir require=False.


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


***

## Wallet
Solo cosuman GET /wallet/create/>qrCODE< 

regresa un pkpass.pkpass


## Empresa

### Dar de Alta Equipo de Seguridad 

Para esto es necesario, el Id del Area a la que se asignara este equipo de Seguridad, y el nombre del equipo de seguridad que desea dar de alta.


**Request:** POST

**url:** http://127.0.0.1:8000/addSecurityEquipment 

**header:** 'authorization: Token cfbced0fc65d1a3d2ba8044dc3035d146603c874' Este token tiene que ser de un administrador solamente.

**json Ejemplo:**

```json
{
	"nameEquipment": "Chaleco Seguridad",
	"idArea":2
}
```








