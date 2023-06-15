## Iber Ismael Piovani

API v1 Documentation

## Objetivo

Tomar los datos de paises de una API externa y los guarda en una base de datos Postgresql.
Mejorar y actualizar esta lista agregando los datos de actividades y permitiendo el envio por mail de los datos de la lista o la descargar.
api: https://restcountries.com/v3.1/all

## Requerimientos

- Python 3.8 o superior

- [fastapi](https://fastapi.tiangolo.com/)
- [uvicorn](https://www.uvicorn.org/)
- [SQLAlchemy](https://www.sqlalchemy.org/)
- [psycopg2](https://www.psycopg.org/)
- [requests](https://docs.python-requests.org/en/master/)
- [python-dotenv](https://pypi.org/project/python-dotenv/)
- [pandas](https://pandas.pydata.org/)
- [pydance](https://pypi.org/project/pydantic/)
- [openpyxl](https://openpyxl.readthedocs.io/en/stable/)
- [secure-smtplib](https://pypi.org/project/secure-smtplib/)
- [apscheduler](https://apscheduler.readthedocs.io/en/stable/)
- [logging](https://docs.python.org/3/library/logging.html)
- [fastapi-cache2](https://pypi.org/project/fastapi-cache2/)
- [cachetools](https://pypi.org/project/cachetools/)

## Uso

- Clonar el repositorio

```
git clone
```

- Crear un entorno virtual

```
python -m venv venv
```

- correr Docker de SQL Server

Colocar el puerto 5432, yo utilize otro por que ya tenia ocupado ese.

```
docker run -d --name paises_vemo -v my_db:/var/lib/postgresql/data_vemo -p 5000:5432  -e POSTGRES_PASSWORD=postgres -e POSTGRES_USER=postgres -e POSTGRES_DB=vemo_pais postgres
```

- test ddbb

```
docker exec -it paises_vemo psql -p 5432 -h localhost -U postgres -W vemo_pais
```

- Instalar las dependencias

```
pip install -r requirements.txt
```

- cargar las credenciales de la base de datos en el archivo `.env`

- Correr el servidor FastAPI con Uvicorn. El servidor se ejecutará en el puerto 8000.

```
main.py
```

## Endpoints

### Root

- URL: `/api/v1/`

### Mostrar todos los países

Retorna una lista con todos los países disponibles.

- Método: GET
- URL: `/api/v1/paises`
- Respuesta exitosa:
  - Código: 200 (OK)
  - Contenido: Lista de países en formato JSON

### Países por ID

Retorna la información de un país específico basado en su ID.

- Método: GET
- URL: `/api/v1/paises/{id}`
- Parámetros de URL:
  - `id`: ID del país
- Respuesta exitosa:
  - Código: 200 (OK)
  - Contenido: Información del país en formato JSON

### Buscador de países

Permite buscar países por nombre, capital o continente.

- Método: GET
- URL: `/api/v1/paises`
- Parámetros de consulta:
  - `nombre`: Filtra los países por nombre (opcional)
  - `capital`: Filtra los países por capital (opcional)
  - `continente`: Filtra los países por continente (opcional)
- Respuesta exitosa:
  - Código: 200 (OK)
  - Contenido: Lista de países que coinciden con los criterios de búsqueda en formato JSON

### Crear actividad

Crea una nueva actividad.

- Método: POST
- URL: `/api/v1/actividades`
- Cuerpo de la solicitud: Datos de la actividad en formato JSON
- Respuesta exitosa:
  - Código: 201 (Created)
  - Contenido: Datos de la actividad creada en formato JSON

### Actualizar actividad

Actualiza una actividad existente.

- Método: PUT
- URL: `/api/v1/actividades/{id}`
- Parámetros de URL:
  - `id`: ID de la actividad
- Cuerpo de la solicitud: Datos actualizados de la actividad en formato JSON
- Respuesta exitosa:
  - Código: 200 (OK)
  - Contenido: Datos de la actividad actualizada en formato JSON

### Borrar actividad

Elimina una actividad existente.

- Método: DELETE
- URL: `/api/v1/actividades/{id}`
- Parámetros de URL:
  - `id`: ID de la actividad
- Respuesta exitosa:
  - Código: 204 (No Content)

### Ver todas las actividades

Retorna una lista con todas las actividades disponibles.

- Método: GET
- URL: `/api/v1/actividades`
- Respuesta exitosa:
  - Código: 200 (OK)
  - Contenido: Lista de actividades en formato JSON

### Utilidades

Envio de mail con excel y descarga de excel

- Método: GET
- URL: `/api/v1/exportar/?correo=`
- Parámetros de URL:
  - `?correo=`: correo electronico
- Respuesta exitosa:
  - Código: 200 (OK)
  - Contenido: Mail enviado con excel

Descarga de excel

- Método: GET
- URL: `/api/v1/descargas`
- Respuesta exitosa:
  - Código: 200 (OK)
  - Contenido: archivo excel

### Scheduler

Estado scheduler

- Método: GET
- URL: `/api/v1/scheduler`
- Respuesta exitosa:
  - Código: 200 (OK)
  - Contenido: En funcionamiento o Detenido

Start scheduler inicia la actualizacion de la base de datos cada 24 horas
o por el tiempo que nosotros le asignemos en segundos.

- Método: GET
- URL: `api/v1/schedulerstart/?segundos=`
- Parámetros de URL:
  - `?segundos=`: tiempo en segundos de intervalo de actualizacion
- Respuesta exitosa:
  - Código: 200 (OK)
  - Contenido: En funcionamiento o Iniciando

Stop scheduler

- Método: GET
- URL: `/api/v1/schedulerstop`
- Respuesta exitosa:
  - Código: 200 (OK)
  - Contenido: Detenido o Deteniendo

## Cache

Se utilizo fastapi-cache2 junto a memcached y cachetools para la cache de los endpoints de paises y actividades.
La cache se inicia al iniciar el servidor y se actualiza cada 60 minutos o cuando se actulizan los datos de la base datos.

## Scheduler

Se utilizo apscheduler para la ejecucion de la actualizacion de la base de datos cada 24 horas. Se utilizo una clase para la creacion del scheduler que permite controlar inicio, fin y estado.
Se implemento un sistema de logging para controlar los eventos, inicio, fin, carga de datos, envio de mail.

## Contacto

- [Linkedin](https://www.linkedin.com/in/iber-ismael-piovani-8b35bbba/)
- [Twitter](https://twitter.com/laimas)
- [Github](https://github.com/Vosinepi)

```

```
