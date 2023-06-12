import sys
import uvicorn
import json
from fastapi import FastAPI, Depends


from app.v1.router.paises import router as paises
from v1.router.busqueda import router as busqueda
from v1.router.pais_detalle import router as pais_detalle

# from v1.router.startup_event import router as startup_event

app = FastAPI()

# @app.on_event("startup")
# def startup_event():
#     create_table()
#     cargar_datos()


@app.get("/")
def root():
    with open("./app/v1/utils/data.json") as file:
        data = json.load(file)
    return data


app.include_router(paises)
app.include_router(pais_detalle)
app.include_router(busqueda)

if __name__ == "__main__":
    try:
        uvicorn.run("main:app", host="localhost", port=8000, reload=True)
    except KeyboardInterrupt:
        sys.exit()
