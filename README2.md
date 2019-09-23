# EndPoints

## Crear Invitacion

**URL**: <urlHost>/create_inv/

**Descripcion:** Creara una invitacion tipo 0.
```json
{
	"areaId": 1,
	"secEquip":"",
	"cellNumber":44437385875,
	"email":"jaha.devcrack@gmail.com",
	"dateInv":"2019-09-23",
	"timeInv":"12:03",
	"exp":null,
	"subject":"nada en particular",
	"vehicle":false,
	"notes": "ninguna",
	"companyFrom": "daelabs",
	"employeeId":1,
	"diary":"",
	"typeInv":""  ##Este campo es opcional, es decir se puede poner o no,  por default toma el valor 0
}
```

## Cargar la informacion de Un Usuario Por Token.

**URL**: <urlHost>/getUser/**Token**/

**Descripcion:** Retornara la informacion necesaria para validar al nuevo usuario.

