# Despliegue DJANGO App en AWS

## Project Settings - Configuracion del Proyecto

```ALLOWED_HOSTS```. Define una lista de direcciones de servidores o bien dominios que pueden ser usados con la instancia DJANGO. Cualquier Peticion que provenga de un HOST que no se encuentra en la lista, desencadenara una excepcion. Se requiere configurar esto para prevenir cualquier vulnerabilidad de seguridad.

**Nota** Asegurese de incluir localhost como una de las opciones en la lista, ya que se requiere para las conexiones proxy con nginx.

Ejemplo:

```
~/myprojectdir/myproject/settings.py
. . .
# The simplest case: just add the domain name(s) and IP addresses of your Django server
# ALLOWED_HOSTS = [ 'example.com', '203.0.113.5']
# To respond to 'example.com' and any subdomains, start the domain with a dot
# ALLOWED_HOSTS = ['.example.com', '203.0.113.5']
ALLOWED_HOSTS = ['your_server_domain_or_IP', 'second_domain_or_IP', . . ., 'localhost']
```


## Configure Database

La configuracion default de django para el origen de datos es para SQLite. Debemos de cambiar esta configuracion para que la instancia django trabaje con PostgresQL.

Instalar **psycopg2** con pip



# Ficha Tecnica

- Amazon RDS 
    - Servicio de seguridad Adminsitrador por Amazon RDS que provee de un gran nivel de seguridad a sus bases de datos.
    - Filtrado de trafico de entrada que provee amazon VPC, grupos 
    -La base de datos esta encriptada, 
    - En las instancias de bases de datos de Amazon con cifrado se utiliza el algoritmo de cifrado AES-256 estándar del sector para cifrar los datos en el servidor que aloja instancias de bases de datos de Amazon RDS. Una vez cifrados los datos, Amazon RDS se encarga de la autenticación de acceso y del descifrado de los datos, con un impacto mínimo en el desempeño.
    - SSL (Capa de conexión segura) o TLS (Transport Layer Security) desde el el api para cifrar la conexión que la base de datos  ejecuta