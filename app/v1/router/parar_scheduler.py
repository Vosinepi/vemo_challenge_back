import sys
from fastapi import Depends, APIRouter, HTTPException

from sqlalchemy.orm import Session

sys.path.append(".")

from app.v1.utils.db import Base, engine, get_db, SessionLocal
from app.v1.model.models import *
from app.v1.schema.schemas import PaisDetalle
from app.v1.scripts.schedule_mail_ddbb import scheduler_mail_ddbb as scheduler

router = APIRouter(prefix="/api/v1/schedulerstop", tags=["scheduler stop"])


@router.get("/")
def stop_scheduler():
    if scheduler and scheduler.running:
        scheduler.stop()
        return {"message": "Se detuvo Scheduler"}
    else:
        return {"message": "Scheduler no se encuentra iniciado"}
