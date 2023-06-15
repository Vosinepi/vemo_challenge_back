import sys
from fastapi import APIRouter

sys.path.append(".")

# modulos propios
from app.v1.model.models import *
from app.v1.scripts.schedule_mail_ddbb import scheduler_mail_ddbb as scheduler

router = APIRouter(prefix="/api/v1/schedulerstop", tags=["scheduler"])


@router.get("/")
def stop_scheduler():
    if scheduler.running == True:
        scheduler.stop()
        return {"message": "Se detuvo Scheduler"}
    else:
        scheduler.stop()
        return {"message": "Scheduler no se encuentra iniciado"}
