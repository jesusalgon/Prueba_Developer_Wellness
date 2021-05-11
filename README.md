# General
## Estructura
Existen dos carpetas principales: *data/* y *src/*. 

- *data/*: Contiene los datos aportados por el usuario. Para añadir entradas a la base de datos, coloca las nuevas medidas en el csv: *data/csv/Monitoring report.csv*.
- *src/*: Contiene el código. Por un lado, los scripts para rellenar la base de datos se encuentran en *src/data_ingestion/*. Por el otro, puedes encontrar el código de la api en *src/django_api/*

## Aspectos técnicos
### API

La API ha sido desarrollada en Python, sobre el framework Django y utilizando recursos en los que se apoya el propio Django para hacer el desarrollo más eficiente. Algunos de ellos son:

- django_rest_framework: Aporta a Django herramientas para el desarrollo de APIs REST.
- django_filters: Permite definir filtros para gestionar el contenido que se envía al usuario y que serán activados mediante los query parameters.
- serializers (Django): Ayudan a serializar los datos que llegan en las llamadas y se envían en las respuestas.
- routers (Django): Ayudan a enrutar de forma más sencilla las llamadas a la api.

Además, la comunicación con la base de datos tiene lugar gracias al ORM de Django a través de un modelo definido en el diseño. A bajo nivel (y en el script de inicialización), la interacción con la base de datos se realiza mediante SQLite, que funciona de forma nativa con Python.

### Algoritmos de volcado a la base de datos
Existen dos scripts que permitirán trasladar los datos del csv a la base de datos.

- parse_and_ingest_db.py: Este es un código de inicialización. Crea la tabla (si no existe) y la rellena mediante SQL con los datos extraidos del csv. También puede usarse para añadir los nuevos datos a la tabla, en caso de que se actualice el csv.
- parse_and_ingest_by_api.py: También sirve para añadir nuevos datos a la tabla, pero esta vez a través de la API (mediante el método POST). Hay que tener precaución, porque muchas llamadas seguidas pueden provocar un error en el servidor.

**Nota:** En ambos casos, se ignoran los datos ya existentes en la base de datos.

**Nota 2:** El código de *parser.py* es utilizado en los dos scripts anteriores para limpiar y formatear los datos antes de enviarlos a la API. Se ha tomado la decisión de dividir la fecha y hora en dos campos distintos para dotar de mayor funcionalidad a la api. Además, los datos de fecha y hora no son únicos para reflejar casos como los cambios de hora de verano e invierno.

## Instalación
### Instalación de paquetes

Para instalar todas las dependencias necesarias, desplázate hasta la carpeta *src/* y utiliza el siguiente comando (asegúrate de tener una versión de Python3 y pip previamente instaladas):

```
pip install -r requirements.txt
```
### Arranque del servidor

Para iniciar el servidor, desplázate hasta la carpeta *src/django_api/* y utiliza el siguiente comando:

```
python manage.py runserver
```

**Nota:** El servidor local se iniciará por defecto en: *http://127.0.0.1:8000/*

# Funcionamiento
## Volcado a la base de datos

Para trasladar los datos de tu csv (que debe estar en *data/csv/Monitoring report.csv*), desplázate hasta la ruta *src/data_ingestion/* y usa el siguiente comando:

```
python parse_and_ingest_db.py
```

Esto provocará que los datos almacenados en el csv se copien a la base de datos ubicada en *src/django_api/wellness.db*, en la tabla *electricity_consumption*. en esta misma base de datos, se alojan también las tablas relacionadas con el funcionamiento de Django.

**Nota:** De la misma manera, puedes usar el script *parse_and_ingest_db.py*, pero es recomendable usar el descrito para la primera ingestión en la tabla.

**Nota 2:** En este caso, la tabla ya está pre-rellenada con datos.

## Comunicación con la API
### Datos del modelo

La API es capaz de madandar y recibir información codificada en JSON en el cuerpo de las llamadas (y respuestas). Esta información debe estar estructurada de la siguiente forma: 

```
{
  "id": int,
  "date": "yyyy-mm-dd",
  "time": "HH:MM:SS",
  "energy": float,
  "reactive_energy": float,
  "power": float,
  "maximeter": float,
  "reactive_power": float,
  "voltage": float,
  "intensity": float,
  "power_factor": float
}
```

Por la naturaleza de la api, todos los campos son obligatorios, a excepción del id, que será la clave principal y se autoincrementa. 

**Nota:** *float* hace referencia a un número decimal. También son válidos números enteros. En cualquier caso, deben ser de signo positivo.

### Create 

Para crear un nuevo recurso, utiliza el método POST directamente sobre la raíz de la API y añade los datos al body:

```
POST http://127.0.0.1:8000/data/
```

**Nota:** En este caso no es necesario (ni recomendable) especificar el id, dado que es una clave que se autoincrementa.

### Retrieve

Para consultar los datos, utiliza el método GET. 

Puedes consultar todos los datos enviando la llamada a la raíz de la API:

```
GET http://127.0.0.1:8000/data/
```

Para filtrar por fecha y hora, puedes utilizar los query parameters *from_date*, *until_date*, *from_time*, *until_time*. Por ejemplo, la siguiente petición devolverá solamente aquellos datos cuya fecha sea mayor o igual al 1 de enero de 2019:

```
GET http://127.0.0.1:8000/data/?from_date=2019-01-01
```

**Nota:** Pueden usarse varios query parameters de forma simultánea.

Además, puedes consultar la información asociada a un id concreto:

```
GET http://127.0.0.1:8000/data/<id_number>/
```
### Update

Para modificar la información de una entrada concreta de la tabla, debes usar PUT e incluir todos los campos (incluso los que no serán modificados) en el body:

```
PUT http://127.0.0.1:8000/data/<id_number>/
```

**Nota:** De nuevo, no es necesario, ni recomendable incluir el id entre los campos del body; pero sí tendrás que conocerlo para hacer la llamada al recurso correcto.

### Delete

Para borrar un recurso, utiliza DELETE:

```
DELETE http://127.0.0.1:8000/data/<id_number>/
```

# Posibles mejoras

Algunas posibles mejoras serían:

- Implementar un filtro para seleccionar un dato concreto de las entradas de la tabla (por ejemplo, 'energy'). Esto podría realizarse mediante más query parameters.
- Implementar una respuesta personalizada para los códigos de estado de la API (solo están implementados los más comunes).
- Implementar un sistema de validación de los datos. Esto puede hacerse sonrecargando las funciones del serializer.
- Hacer que los scripts para volcar datos en la tabla sean capaces de detectar cualquier csv. Esto se puede implementar fácilmente mediante una búsqueda regex con la librería glob.
- Realizar una limpieza más profunda de los datos en el csv. En este caso, se ha supuesto que los datos son correctos (excepto los NaN), incluyendo las fechas y horas duplicadas. Sin embargo, echando un vistazo a los datos, pueden llegar a encontrarse anomalías subsanables (por ejemplo, valores negativos o que no cuadran con las unidades del resto de datos).

# Notas importantes

Dado que es un proyecto que va a ser evaluado, y no puesto en producción, he decidido dejar activos todos los logs de Django y a la vista aspectos como la *djago_secret_key* por si fuera necesario para el evaluador realizar alguna prueba sobre el código.
