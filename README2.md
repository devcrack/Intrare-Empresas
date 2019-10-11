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



# Pendientes

- [ ] Rediseñar Invitaciones.
- [ ] Revisar que todos los EndPoints de invitaciones funcionen de acuerdo a los cambios realizados.
- [ ] Rediseño de Creacion de Usuario Nuevo, solamente con email o con telefono o ambos.
- [ ] Faltas de Ortografia Mensajes.
- [ ] Correos registro y lectura todo en minusculas.
- [ ] En correo Invitacion agregar ademas de la imagen de codigo, el codigo en Texto.
- [ ] Borrar el usuario cuando este no ha sido validado.
- [ ] EndPoint UpdatePlatform User.
- [ ] Equipo de Seguridad por Area.
- [ ] Listar todos aquellos usuarios que no han sido validados y tiene que ser validados por anfitrion.




