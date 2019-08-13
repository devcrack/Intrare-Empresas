# TODOS
POR HACER(INMEDIATO)                                |HACIENDO                                       |HECHO                                                       |PLANEAR                                                             |
----------------------------------------------------|-----------------------------------------------|------------------------------------------------------------|--------------------------------------------------------------------|
Generar link a formulario invitacion por referidos  |Vistas con reestructuracion de las invitaciones|Restructuracion modelos invitaciones para manejar referidos |Agregar caducidad al link de invitacion por referidos               |
Vista accesos                                       |                                               |                                                            |Script para depurar base de datos(Eliminar invitaciones muy viejas) |
Puta aplicacion de mierda                           |                                               |                                                            |Como hacer para que el usuario pueda eliminar sus invitaciones      |


# Acerca de las invitaciones

Existe solo un tipo de invitacion y tiene una sola variacion en su funcionamiento.

### Tabla invitaciones
Invitacion      |Tipo   | OBLIGATORIO   | 
----------------|-------|---------------|           
idInvitacion    |PK     |               |  
idEmpresa       |FK     |SI             |
idArea          |FK     |SI             |
idEmpleado      |FK     |SI             |
fechaEnvio      |DATE   |SI             |
fechaInvitacion |DATE   |SI             |
idUsuario       |FK     |NO             |
asunto          |STRING |SI             |
automovil       |BOOL   |SI             |
empresa         |STRING |NO             |
notas           |STRING |NO             |
LEIDA           |BOOL   |SI/AUTO        |

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
InvitacionReferido  | Tipo   | OBLIGATORIO   | 
--------------------|--------|---------------|
idInvitacionReferido|        |               |
emailTercero        |EMAIL   |SI             |
idInvitacion        |FK      |SI             |
hash_code/LINK      |STRING  |SI             |

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

#### Usuario Registrado

En este caso no existe ninguna anormalidad con las invitaciones, aqui el usuario ya esta registrado en la plataforma
y al generar una invitacion este se vincula con la invitacion mediante su respectiva relacion  FK- > PK

### El usuario No ha realizado el registro completo.

En este caso el usuario no ha creado su registro pero, como normalmente cada vez que se genera una invitacion dicha 
invitacion tiene que especificarse un numero telefonico, se tiene que crear un usuario algo asi como semiregistrado
donde solo especificamos el numero de telefono y el nombre de usario que pasaria a ser su mismo numero de telefono.
Si el usuario llegase a registrarse en la plataforma entonces tendriamos que verifcar si este ya ha sido registrado automaticamente 
por el sistema previamente. De ser asi entonces tendriamos que simplemente actualizar dicho usuario con su respectiva informacion.

### Invitacion mediante Referidos(Terceros)
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
  "notes": "Notas de relativas a la invitacion"
}
```  


















# NUEVO JSON 
  ```json
  {
	"employee_id":2,
	"cell_number":3008269546,
	"email":"leila@example.com",
	"area_id":2,
	"business":"Junta de trabajo con el gerente",
	"sec_equip":"Macana",
	"vehicle":true,
	"company":"Red Sparrow Techologies",
	"date":"2016-01-27 12:05",
	"notes":"foo bar"
}
  ```
# Tipos de Usuario 
* Super Administrador
* Administradores
  * Administradores (Empresa)
  * Administradores Parque.
* Empleado
* Vigilante Empresa, Vigilante Parque


## Acciones por cada tipo de Usuario
### Super Administrador
- [ ] Altas de Parque
- [ ] Modificaciones de Parque
- [ ] Consultas de Parque
    * Despliega listado de todas las empresas 
       y despliega un mayor detalle de la empresa seleccionada ya sea para consulta o modificacion. 
       Ver sistema para mas detalles.
- [ ] Altas de Empresa 
- [ ] Modificaciones de Empresa 
- [ ] Consultas de Empresas
     * Despliega listado de todas las empresas 
       y despliega un mayor detalle de la empresa seleccionada ya sea para consulta o modificacion. 
       Ver sistema para mas detalles.

### Administrador 
- [ ] Altas Empleado
- [ ] Modificaciones Empleado
- [ ] Consultas de Empleado
      * Despliega listado de todos los empleados
       y despliega un mayor detalle del empleado seleccionado ya sea para consulta o modificacion. 
       Ver sistema para mas detalles.
- [ ] Consulta Invitaciones. Ver sistema para mas detalles. **Nota** Puede filtrar invitaciones por fecha.
- [ ] Consulta Accesos. Ver sistema para mas     detalles.
- [ ] Consulta Bitacora. Ver sistema para mas detalles.
- [ ] Genera un tipo de invitacion llamada Invitacion 
      Personal. En el backend una invitacion empresarial.
- [ ] Puede firmar pase de salida(Autorizar accesos).
- [ ] Configura el color de las areas.
- [ ] Alta de Caseta
- [ ] Modificaciones de Caseta.
- [ ] Despliega listado de todas las casetas de la empresa y despliega con mayor detalle de la inforamcion de la caseta seleccionada ya sea para consulta o modificacion. 
- [ ] Alta de Vigilante
- [ ] Modificaciones de Vigilante.
- [ ] Despliega listado de todas las casetas de la empresa y despliega con mayor detalle de la inforamcion de la caseta seleccionada ya sea para consulta o modificacion. 
- [ ] Envia mensaje de emergencia.
- 

