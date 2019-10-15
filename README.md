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
	"companyFrom":"DaeLabs"
}
```

***
## Cargar la informacion de Un Usuario Por Token.

**URL**: <urlHost>/getUser/**Token**/

**Descripcion:** Retornara la informacion necesaria para validar al nuevo usuario.


## Invitaciones Grupales


**URL** <<<<http://127.0.0.1:8000>>>>/create_massiveInv/


**Descripcion:** Genera N invitaciones, en base al numero elementos que contenga el valor del campo\clave guests.
Cada elemento en la lista es un diccionario/json que contiene un par de  clave:valor, **email** y **cellphone**. Ambos valores aqui son totalmente necesarios, ya que en caso de que alguno de estos no exista
se creara un usuario nuevo, y en caso de existir estos valores seran obtenidos directamente de la base de datos. En terminos de logica en base a lo que establecimos(obligar en el preregistro email y numero de celular)
es indiscutible.

**ACCION POST**

**HEADER**  --header 'authorization: Token 58d0f3f11449ba8a958a9ff04b6823784394e494' , donde el token pertenece ya sea a un empleado o a un administrador.



```json
{
  "areaId":1,
  "guests":[
    {
      "email":"andes204@gmail.com",
      "cellphone":4443227734
    },
    {
      "email":"jaha.devcrack@gmail.com",
      "cellphone":4446354597
    }],  
  "subject":"Nada en particular",
  "dateInv":"2019-09-25",
  "timeInv":"12:50",
  "exp":null,
  "diary":"",
  "secEquip":"",
  "vehicle":true,
  "companyFrom":"Bit Composer",
  "notes":"Ni maiz paloma",
  "employeeId":null
}
```

## Notificacion Pase de Salida

**Tipo request** GET \

**url** <<<<http://127.0.0.1:8000>>>>/notifySignExitPass/**IdAcceso**/

**Descripcion:** Genera una notificacion al anfitrion(via sms y email, por el momento) en donde se indica que tiene que firmar un pase de salida a un invitado al que no se la ha firmado pase de salida.


---
***
___

# Generacion de un usuario nuevo mediante el envio de invitacion(Registro automatico)

 1. Anfitrion envia Invitacion
    * Caso A Usuario Existe 
    * Caso B Usuario no Existe
 2. **B** El usuario no existe
   
    1. Crear un Usuario, pero dicho usuario no esta ACTIVO = FALSE
    2. Generar Invitacion 0,
    3. Enviar Solocitud de Preregistro por, email y SMS. **FORMULARIO** , **EndPoint**
    4. Cuando el Usuario complete el Preregistro, enviar notificacion al anfitrion mediante email y sms, mostrando los datos que se han dado de alta de dicho usuario, para validar su identidad.
       **Formulario y EndPoint** 
    5. Una vez que el anfitrion valide la identidad Activar el usuario **EndPoint ACTIVAR USUARIO**
       - Cuando se activa al usuario se envia su invitacion 0 con su contraseña temporal.



# Acerca de las invitaciones

## Consideraciones

- Se tiene que especificar:
  - Una fecha de la visita. 
  - Una hora de la visita.
- Todas las invitaciones tienen caducidad, por default la caducidad es 2 dias despues de que se genero la invitacion.
- La validacion o creacion se realiza ya sea mediante email o numero telefonico celular.

## User.is_active == False

Si el usuario no ha sido activado, mediante el preRegistro que tiene que realizar el usuario, entonces las invitaciones no se le enviaran
solo se enviara la notificacion de que se tiene que registrar.

## User.is_active == True

El usuario ha sido activado, el usuario se ha Preregistrado, entonces se envian las notificaciones de invitaciones normalmente.


Existe solo un tipo de invitacion y tiene una sola variacion en su funcionamiento.

### Tabla invitaciones
| Invitacion      | Tipo     | OBLIGATORIO |
|-----------------|----------|-------------|
| idInvitacion    | PK       |             |
| idEmpresa       | FK       | SI          |
| idArea          | FK       | SI          |
| idEmpleado      | FK       | SI          |
| typeInv         | INT      | SI          |
| dateInv         | DATE     |             |
| timeInv         | TIME     | SI          |
| expiration      | DATE     | SI          |
| diary           | String   | NO          |
| idUsuario       | FK       | NO          |
| asunto          | STRING   | SI          |
| automovil       | BOOL     | SI          |
| empresa         | STRING   | NO          |
| notas           | STRING   | NO          |
| LEIDA           | BOOL     | SI/AUTO     |



Cada Invitacion tiene que cubrir con los campos que son marcados como obligatorios sin excepcion,
ya que son totalmente necesarios para gestionar las invitaciones.

#### Descripcion de los campos
- idInvitacion Clave unica auto incrementable
- idEmpresa: Clave foranea de la empresa a donde se esta invitando.
- idArea : Clave foranea del area de la empresa a donde se esta invitando.
- idEmpleado: Empleado que funge como anfitrion, obviamente perteneciente a la empresa donde se esta invitando.
- fechaEnvio/Invitacion: Fecha y hora de de envio de la invitacion /  Fecha y hora que acontecera la invitacion.
- idUsuario: Clave foranea que referencia al usuario que es el invitado.
- asunto: Asunto a tratar en la visita relativa a la invitacion.
- automovil: Bandera que indica si el invitado vendra con automovil.
- empresa: Compañia de donde proviene el visitante.
- notas: Notas extra relativas a la invitacion.
- LEIDA : Bandera que indica si el invitado a verificado la invitacion.

### Tabla InvitacionReferido
| InvitacionReferido   | Tipo   | OBLIGATORIO |
|----------------------|--------|-------------|
| idInvitacionReferido |        |             |
| emailTercero         | EMAIL  | SI          |
| idInvitacion         | FK     | SI          |
| hash_code/LINK       | STRING | SI          |

Esta tabla cumple con una funcion especial. Se usa cuando se delega el hacer la invitacion aun tercero, externo a la empresa
invitadora. 
Al generar un registro en esta tabla, se crea una invitacion pero con un usuario vacio, es decir dicha invitacion no esta vinculada a ningun usuario
por el momento. Al enviar la invitacion mediante un **emailTercero** solamente hacemos un preregistro con lo que se da de alta una invitacion, 
el asignar un usuario a esa invitacion se lo delegamos al propietaro del **emailTercero** que es quien completara el registro 100 x 100.

#### Descripcion de los campos
- idInvitacionReferido: Clave primaria
- emailTercero: Email de la persona a quien delegamos completar el registro de la invitacion.
- idInvitacion: Clave foranea de la invitacion con la que se ha creado el preregistro.
- hascodeLink: Codigo especial que sirve para proteger el enlace que llevara al tercero al formulario para completar el registro de la invitacion(AQUI se crea un usario y se vincula a la invitacion). 

## Casos especiales con las invitaciones
Las invitaciones siempre estaran vinculadas a un usuario, aunque el campo este como que puede ser nulo, de alguna u otra 
forma siempre estara vinculado a un usuario. De otra manera la invitacion no tiene razon de ser.
Las invitaciones siempre estan relacionadas con el usuario mediante su respectivo **idUsuario**.

Siempre que se intente generar una invitacion siempre 100x100 se tiene que proporcionar un numero telefonico. Dado que el numero telefonico es un campo unico
e irrepetible, podemos identificar si un usuario ya se ha registrado a la plaforma mediante su numero telefonico :metal .

#### Usuario Registrado INVITACIONES TIPO 0

En este caso no existe ninguna anormalidad con las invitaciones, aqui el usuario ya esta registrado en la plataforma
y al generar una invitacion este se vincula con la invitacion mediante su respectiva relacion  FK- > PK

### El usuario No ha realizado el registro completo. 

En este caso el usuario no ha creado su registro pero, como normalmente cada vez que se genera una invitacion dicha 
invitacion tiene que especificarse un numero telefonico, se tiene que crear un usuario algo asi como semiregistrado
donde solo especificamos el numero de telefono y el nombre de usario que pasaria a ser su mismo numero de telefono.
Si el usuario llegase a registrarse en la plataforma entonces tendriamos que verifcar si este ya ha sido registrado automaticamente 
por el sistema previamente. De ser asi entonces tendriamos que simplemente actualizar dicho usuario con su respectiva informacion.

### Invitacion mediante Referidos(Terceros) INVITACIONES TIPO 1
Aqui se da de alta una invitacion pero sin especificar el usuario, solamente registramos los campos obligatorios de la 
invitacion realizando un preregistro de la invitacion. Se tiene que especificar un correo electronico que pertenece a un 
referido o un tercero que es la persona a la que delegamos la tarea de vincular la invitacion creada aun usuario
completando totalmente el registro de la invitacion.


## JSON's para la Creacion de Invitaciones

### Invitaciones REGISTRO COMPLETO

Este tipo de invitaciones son creadas por un usuario de la plataforma, es decir ya sea por un Administrador o un empleado,,
que hace uso del sistema.

Para que generar una invitacion caso **Administrador** genera la invitacion el json que recibe el  el API es el siguiente:
 ```json
{
  "areaId": 3,
  "employeeId":2,
  "dateInv": "2016-01-27 12:05",
  "numCell": 4443424829,
  "subject": "Algun asunto de la visita",
  "secEquip": "1,3,6",
  "vehicle": false,
  "companyFrom": "Edison Effect",
  "notes": "Notas de relativas a la invitacion"
}
 ```

En donde 
- areaId: Identificador del area donde se va hacer la visita
- employeeId: Identificador del empleado que esta generando la visita.
- dateInv: Fecha de cuando se llevara acabo la visita.
- numCell: Numero de telefono **Celular** del visitante(Usuario).
- subject: Razon por la cual se hace la visita.
- secEquip: Cadena con los identificadores de los equipos de seguridad, separado por comas  en caso de ser varios. 
- vehicle": Indica si el visitante lleva vehiculo o no.
- companyFrom: Compañia de donde  proviene el visitante. **Puede dejarse en blanco/null** en caso de no tener definido esto. 
- notes: Notas de relativas a la invitacion. 

Generar una invitacion caso **Empleado** genera la invitacion el json que recibe el  el API es el siguiente:

 
 ```json
{
  "areaId": 3,
  "employeeId":null,
  "dateInv": "2016-01-27 12:05",
  "numCell": 4443424829,
  "subject": "Algun asunto de la visita",
  "secEquip": "1,3,6",
  "vehicle": false,
  "companyFrom": "Edison Effect",
  "notes": "Notas de relativas a la invitacion"
}
 ``` 
Como se puede observar es el mismo json que se discutio previamente, con la unica diferencia de que employeeId es null 
ya que este valor se obtiene a traves del token de sesion.


### Invitaciones PreRegistro/Referidos-Terceros

Estas invitaciones igualmente son generadas por un usuario del sistema (Administrador/Empleado) pero aqui se le confiere
la asignacion de un usuario(el invitado) a un tercero que es quien completa el registro del usuario para esta invitacion.


### Json Invitacion por Referidos **Administrador**:
 ```json
{
  "areaId": 3,
  "employeeId":2,
  "dateInv": "2016-01-27 12:05",
  "subject": "Algun asunto de la visita",
  "secEquip": "1,3,6",
  "vehicle": false,
  "companyFrom": "Edison Effect",
  "notes": "Notas de relativas a la invitacion",
  "mail": "dir@mail.com"
}
```  


### Json Invitacion por Referidos **Empleado**:
 ```json
{
  "areaId": 3,
  "employeeId":null,
  "dateInv": "2016-01-27 12:05",
  "subject": "Algun asunto de la visita",
  "secEquip": "1,3,6",
  "vehicle": false,
  "companyFrom": "Edison Effect",
  "notes": "Notas de relativas a la invitacion",
  "mail": "dir@mail.com"
}
```  

## EndPoints 
#### URL_HOST/get_inv/user

Return all invitations that a simple user has.

Example Json obtained from this EndPoint.

```json
 {
    "companyName": "Ross Group",
    "areaName": "Gerencia",
    "hostFirstName": "Brent",
    "hostLastName": "Lewis",
    "fecha_hora_invitacion": "2019-08-18T00:00:00-05:00",
    "asunto": "Recently example executive minute despite value. National action team do chance.\nImage person rest boy. Despite final watch imagine blood win. Though serve business follow nothing before.",
    "automovil": false
  }
```

# Notas del Desarrollador(JAHA-DEVCRACK)
## Creacion Invitaciones.

JSON Usado para la creacion de las invitaciones.

```json
{
 "areaId": 3,
 "employeeId":2,
 "dateInv": "2016-01-27 12:05",
 "numCell": 4443424829,
 "email": "unemail@mail.com",
 "subject": "Algun asunto de la visita",
 "typeInv":can be null, default = 0
 "dateInv":"Yy-Mm-Dd",can be null, default = (Al dia siguiente)
 "timeInv": "Hh:Mm", Default misma hora enviada invitacion
 "exp": "Yy-Mmm-Dd", Default = (2 dias despues de que se envia la invitacion")
 "secEquip": "1,3,6",
 "vehicle": false,
 "companyFrom": "Edison Effect",
 "notes": "Notas de relativas a la invitacion"
}
```

Informacion necesaria para crear las invitaciones


-  areaId
- idEmpresa
- idEmpleado
- fechaInvitacion
- idUsuario....Este campo puede estar vacio
- asunto
- automovil
- empresa
- notas

## Tareas devcrack.
- [X] Cambiar validador de json
- [X] Crear Invitaciones como administrador

## sheet Terminator

### Dividir Horizontalmente
Shitf + Ctrl + O
### Dividir Verticalmente
Shitf + Ctrl + E
### Editar Titulo Pestaña
Ctrl + Alt + A
### Editar Titutlo Terminal
Ctrl + Alt + X
### Editar Titulo Ventana
Ctrl + Altf + W

## Django Docs

### About Models

## About API
### Types of users

- Roll 5: Administrador Empresa 
- Roll 4 : Administrador Parque
- Roll 3 : Vigilante Parque.
- Roll 2: Simple Vigilante.
- Roll 1: Empleado.
- Roll 0, Staff & SuperUser = False : Simple User.

## Credencials api 

### Asus Rog

|email                     |token                                        |typeUser  |
|--------------------------|---------------------------------------------|----------|
|16bdaempleado@mail.com    | eebd94cb84f227632520acc44fa4373d3bac8b0e     |Empleado  |
|d3e42simple_user@mail.com | efb4e287751d855eba8a212d00ff506ce425fa72     |SimpleUser|


# EndPoints 

## Creacion de Usuario

    **HEADER** 

    none

    **URL**

    host_url/UserPlatformCreate/

    **JSON**

    ```json
    {
	  "username":"prueba1@mail.com",
	  "password":"mientras123",
	  "first_name":"aurelio",
	  "last_name":"hernandez",
	  "celular":1234532,
	  "email": "aurelio.hdz.aguilar@gmai.com"
  }
    ```

    Tipo Request: Post

## Actualizacion de Usuario

    **HEADER**

     Authorization Token #"$

    **URL**

    host_url/UserPlatformUpdate/

    **JSON**

    ```json
    {
        "email": "newValue",
        "username": "newValue",
        "first_name": "newValue",
        "last_name": "newValue",
        "celular": newValue
    }
    ```

    Tipo Request: Patch

## Actualizacion de Password

  **HEADER**

  Authorization Token #"$

  **URL**

  host_url/UserPasswordUpdate/

  **JSON**

  ```json
  {
	"password": "newValue"
  }
  ```
  
  Tipo Request: Patch


##  Actualizacion de Usuario Imgen Ine(Frente/Atras)

   **HEADER**
   
   - Authorization Token #"$

   - multipart/form-data

   **URL**

   host_url/UserImgUpdate/

   Tipo Request: Patch

   **Body**

   Content type:multipart/form-data

   Fields:
   - imgFront: 'pathFile'
   - imgBack: 'pathFile' 

## Actualizacion de Avatar(Profile pic)   

**HEADER**
   
   - Authorization Token #"$

   - multipart/form-data

   **URL**

   host_url/AvatarUpdate/

   Tipo Request: Patch

   **Body**

   Content type:multipart/form-data

   Fields:
   - img: 'pathFile'


# Acerca de los usuarios

### Usuario
| CustomUser    | Tipo              | OBLIGATORIO  |
|---------------|-------------------|--------------|
| email         | EmailField        | NO           |
| celular       | CharField(String) | SI           |
| ine_atras     | ImageField        | NO           |
| ine_frete     | ImageField        | NO           |
| avatar        | ImageField        | NO           |
| roll          | IntegerField      | SI           |
| temporalToken | CharField         | NO           |
| plataform     | CharField(String) | REDUNTANDTE? |
| username      | CharField(String) | SI           |
| first_name    | CharField(String) | NO           |
| last_name     | CharField(String) | NO           |


### Wallet
solo cosuman GET /wallet/create/<qr> regresa un pkpass.pkpass





