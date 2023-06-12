import sys
import uvicorn
from fastapi import FastAPI, Depends, APIRouter
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session, joinedload

from v1.utils.db import Base, engine, get_db, SessionLocal

sys.path.append(".")

from v1.scripts.create_table import create_table
from v1.scripts.cargar_datos import cargar_datos

from v1.model.models import *
from v1.schema.schemas import PaisLista

router = APIRouter(tags=["Crear_Cargar"])


@router.on_event("startup")
def startup_event():
    create_table()
    cargar_datos()
