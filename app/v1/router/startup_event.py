import sys

from fastapi import APIRouter
from apscheduler.schedulers.background import BackgroundScheduler

sys.path.append(".")

from v1.scripts.create_table import create_table
from app.v1.scripts.carga_paises import cargar_datos

from app.v1.scripts.eschedule_mail_ddbb import actualizar_enviar_correo

from v1.model.models import *


router = APIRouter(tags=["Crear_Cargar"])


@router.on_event("startup")
async def startup_event():
    create_table()
    cargar_datos()

    # tarea de actualizacion diaria de datos y envio de mail
    scheduler = BackgroundScheduler()
    scheduler.add_job(actualizar_enviar_correo, "interval", hours=24)
    scheduler.start()
