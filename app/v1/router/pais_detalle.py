import sys
from fastapi import Depends, APIRouter, HTTPException
from sqlalchemy.orm import Session

# Decorador para cachear la respuesta de la función
from fastapi_cache.decorator import cache

sys.path.append(".")

# Modulos propios
from app.v1.utils.db import Base, engine, get_db, SessionLocal
from app.v1.model.models import *
from app.v1.schema.schemas import PaisDetalle

router = APIRouter(prefix="/api/v1/paises/{id}", tags=["paises"])


@router.get("/", response_model=PaisDetalle)
@cache(expire=3600)
def get_pais(id: int, db: Session = Depends(get_db)):
    pais = db.query(Pais).filter(Pais.id == id).first()

    if not pais:
        raise HTTPException(status_code=404, detail="País no encontrado")

    actividades_dict = [
        {
            "nombre": actividad.nombre,
            "descripcion": actividad.descripcion,
            "paises_con_actividad": [pais.nombre for pais in actividad.paises],
        }
        for actividad in pais.actividades
    ]
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
