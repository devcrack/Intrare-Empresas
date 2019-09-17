# TODOS
| POR HACER(INMEDIATO)                               | HACIENDO                                        | HECHO                                                       | PLANEAR                                                             |
| -------------------------------------------------- | ----------------------------------------------- | ----------------------------------------------------------- | ------------------------------------------------------------------- |
| Generar link a formulario invitacion por referidos | Vistas con reestructuracion de las invitaciones | Restructuracion modelos invitaciones para manejar referidos | Agregar caducidad al link de invitacion por referidos               |
| Vista accesos                                      |                                                 |                                                             | Script para depurar base de datos(Eliminar invitaciones muy viejas) |
| Puta aplicacion de mierda                          |                                                 |                                                             | Como hacer para que el usuario pueda eliminar sus invitaciones      |


# Acerca de las invitaciones

## User.is_active == False

Si el usuario no ha sido activado, mediante el preRegistro que tiene que realizar el usuario, entonces las invitaciones no se le enviaran
solo se enviara la notificacion de que se tiene que registrar.

## User.is_active == True

El usuario ha sido activado, el usuario se ha Preregistrado, entonces se envian las notificaciones de invitaciones normalmente.


Existe solo un tipo de invitacion y tiene una sola variacion en su funcionamiento.

### Tabla invitaciones
| Invitacion      | Tipo   | OBLIGATORIO |
|-----------------|--------|-------------|
| idInvitacion    | PK     |             |
| idEmpresa       | FK     | SI          |
| idArea          | FK     | SI          |
| idEmpleado      | FK     | SI          |
| fechaInvitacion | DATE   | SI          |
| idUsuario       | FK     | NO          |
| asunto          | STRING | SI          |
| automovil       | BOOL   | SI          |
| empresa         | STRING | NO          |
| notas           | STRING | NO          |
| LEIDA           | BOOL   | SI/AUTO     |

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
 "subject": "Algun asunto de la visita",
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








