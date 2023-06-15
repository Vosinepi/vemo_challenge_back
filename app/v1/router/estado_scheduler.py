import sys
from fastapi import APIRouter

sys.path.append(".")

# modulos propios
from app.v1.scripts.schedule_mail_ddbb import scheduler_mail_ddbb as scheduler

router = APIRouter(prefix="/api/v1/scheduler", tags=["scheduler"])


@router.get("/")
def estado_scheduler():
    return scheduler.estado()  # devuelve el estado del scheduler
