import sys
from fastapi import APIRouter

sys.path.append(".")

# modulos propios
from app.v1.model.models import *
from app.v1.scripts.schedule_mail_ddbb import scheduler_mail_ddbb as scheduler

router = APIRouter(prefix="/api/v1/schedulerstart", tags=["scheduler"])


@router.get("/")
def start_scheduler(segundos: int = 86400):
    if not scheduler.running:
        scheduler.start(segundos)
        return {"message": "Se inicio Scheduler"}
    else:
        scheduler.start(segundos)
        return {"message": "Scheduler ya se encuentra iniciado"}
