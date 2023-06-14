import sys
import uvicorn
import json
from fastapi import FastAPI


from v1.router.paises import router as paises
from v1.router.busqueda import router as busqueda
from v1.router.pais_detalle import router as pais_detalle
from v1.router.startup_event import router as startup_event
from v1.router.enviar_excel import router as enviar_excel
from v1.router.descarga import router as descarga
from v1.router.estado_scheduler import router as estado_scheduler
from v1.router.arrancar_scheduler import router as arrancar_scheduler
from v1.router.parar_scheduler import router as parar_scheduler
from v1.router.crear_actividad import router as crear_actividades

app = FastAPI(title="API Paises", version=0.1, root_path="/")


@app.get("/api/v1")
def root():
    with open("./app/v1/utils/data.json") as file:
        data = json.load(file)
    return data


# Routers
app.include_router(
    startup_event
)  # Este router se ejecuta al iniciar el servidor crea tabla y carga datos y deja una tarea programada para actualizar los datos y enviar correo
app.include_router(paises)  # Listado de paises
app.include_router(pais_detalle)  # Detalle de un pais
app.include_router(busqueda)  # Busqueda de paises por nombre
app.include_router(crear_actividades)  # Crear actividades
app.include_router(enviar_excel)  # Enviar excel por correo
app.include_router(descarga)  # Descargar excel
app.include_router(estado_scheduler)  # Estado del scheduler
app.include_router(arrancar_scheduler)  # Arrancar el scheduler
app.include_router(parar_scheduler)  # Parar el scheduler

if __name__ == "__main__":
    try:
        uvicorn.run("main:app", host="localhost", port=8000, reload=True)
    except KeyboardInterrupt:
        sys.exit()
