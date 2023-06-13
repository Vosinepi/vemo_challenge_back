import sys
from fastapi import Depends, APIRouter, HTTPException

from sqlalchemy.orm import Session

sys.path.append(".")

from app.v1.utils.db import Base, engine, get_db, SessionLocal
from app.v1.model.models import *
from app.v1.schema.schemas import PaisDetalle

router = APIRouter(prefix="/api/v1/paises/{}", tags=["pais"])


@router.get("/", response_model=PaisDetalle)
def get_pais(pais_id: int, db: Session = Depends(get_db)):
    pais = db.query(Pais).filter(Pais.id == pais_id).first()

    if not pais:
        raise HTTPException(status_code=404, detail="País no encontrado")

    actividades_dict = [{"nombre": actividad.nombre} for actividad in pais.actividades]
    idiomas_dict = [{"nombre": idioma.nombre} for idioma in pais.idiomas]
    continente_dict = [{"nombre": continente.nombre} for continente in pais.continente]

    pais_dict = {
        "id": pais.id,
        "capital": pais.capital,
        "moneda": pais.moneda,
        "bandera": pais.bandera,
        "nombre": pais.nombre,
        "poblacion": pais.poblacion,
        "actividades": actividades_dict,
        "continente": continente_dict,
        "idiomas": idiomas_dict,
    }

    return {"pais": [pais_dict]}
