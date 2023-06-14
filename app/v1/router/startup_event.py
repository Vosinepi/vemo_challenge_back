import sys

from fastapi import APIRouter


sys.path.append(".")

from v1.scripts.create_table import create_table
from app.v1.scripts.carga_paises import cargar_datos
from app.v1.scripts.schedule_mail_ddbb import scheduler_mail_ddbb as scheduler

from v1.model.models import *


router = APIRouter(tags=["Crear_Cargar"])


@router.on_event("startup")
async def startup_event():
    create_table()
    cargar_datos()

    # tarea de actualizacion diaria de datos y envio de mail
    scheduler.start()
