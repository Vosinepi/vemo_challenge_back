import sys

from fastapi import APIRouter


sys.path.append(".")

from v1.scripts.create_table import create_table
from app.v1.scripts.carga_paises import cargar_datos
from app.v1.scripts.schedule_mail_ddbb import scheduler_mail_ddbb as scheduler

router = APIRouter(prefix="/api/v1/scheduler", tags=["scheduler"])


@router.get("/")
def estado_scheduler():
    return scheduler.estado()  # devuelve el estado del scheduler
