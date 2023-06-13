import sys
from fastapi import Depends, APIRouter
from sqlalchemy.orm import Session, joinedload

sys.path.append(".")

from app.v1.utils.db import get_db
from app.v1.model.models import Actividad, PaisActividad
from app.v1.schema.schemas import PaisLista, Actividad

router = APIRouter(prefix="/api/v1/crear_actividades", tags=["paises"])
