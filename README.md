# TODOS
POR HACER(INMEDIATO)                                                           |HACIENDO                                                  |PLANEAR|
----------------------------------------------------------------------|-------------------------------------------------------------------|-----------------------------------------------------------------------|
Vistas con reestructuracion de las invitaciones                       |Restructurando modelos invitaciones para manejar referidos         |Agregar caducidad al link de invitacion por referidos                  |
Generar link a formulario invitacion por referidos                    |                                                                   | Script para depurar base de datos(Eliminar invitaciones muy viejas)   |
Vista Accesos                                                         |                                                                   |Como hacer para que el usuario pueda eliminar sus invitaciones         |
                                                                      |

## Acerca de las invitaciones
Existe solo un tipo de invitacion pero con sus respectivas variantes de acuerdo a unas caracteristicas
especiales. Dichas caracteristicas vienene dadas por la siguiente tabla:

### Tabla invitaciones
Invitacion      |Tipo   | OBLIGATORIO   | 
----------------|-------|---------------|           
idInvitacion    |PK     |               |  
idEmpresa       |FK     |SI             |
idArea          |FK     |SI             |
idEmpleado      |FK     |SI             |
fechaEnvio      |DATE   |SI             |
fechaInvitacion |DATE   |SI             |
numTelefono     |STRING |NO             |
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
- numTelefono del invitadio(Usuario). Este sera usado como clave foranea que referencia al usuario que es el invitado.
- asunto: Asunto a tratar en la visita relativa a la invitacion.
- automovil: Bandera que indica si el invitado vendra con automovil.
- empresa: Compañia de donde proviene el visitante.
- notas: Notas extra relativas a la invitacion.
- LEIDA : Bandera que indica si el invitado a verificado la invitacion.

### Tabla InvitacionReferido
InvitacionReferido  | Tipo   | OBLIGATORIO   | 
--------------------|--------|---------------|
idInvitacionReferido|        |
emailTercero        |EMAIL   |SI             |
idInvitacion        |FK      |SI             |
hash_code/LINK      |STRING  |SI             |




### Casos
#### NUMERO TELEFONICO
Siempre cada invitacion va a estar vinculada a un numero telefonico, siempre sin excepcion.

 sin importar si tiene un registro 
mediante la aplicacion(en este caso el , o si no se 
ha registrado con la aplicacion se genera un usuario siempre  a partir de su numero telefonico.
En este caso cuando se hace el registro mediante el numero telefonico  a lo cual llamamos Semiregistro. El semiregistro se tiene que verificar cuando el usuario se ha registrado mediante la aplicacion
para asi poder actualizar su informacion y realizar un registro completo.


























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

