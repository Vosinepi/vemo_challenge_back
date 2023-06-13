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

app = FastAPI(title="API Paise", version=0.1, root_path="/")


@app.get("/api/v1")
def root():
    with open("./app/v1/utils/data.json") as file:
        data = json.load(file)
    return data


# Routers
app.include_router(
    startup_event
)  # Este router se ejecuta al iniciar el servidor crea tabla y carga datos
app.include_router(paises)  # Listado de paises
app.include_router(pais_detalle)  # Detalle de un pais
app.include_router(busqueda)  # Busqueda de paises por nombre
app.include_router(enviar_excel)  # Enviar excel por correo
app.include_router(descarga)  # Descargar excel

if __name__ == "__main__":
    try:
        uvicorn.run("main:app", host="localhost", port=8000, reload=True)
    except KeyboardInterrupt:
        sys.exit()
