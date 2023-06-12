from fastapi import Depends, APIRouter
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session, joinedload

from v1.utils.db import Base, engine, get_db, SessionLocal


from v1.model.models import *
from v1.schema.schemas import PaisLista

router = APIRouter(prefix="/paises", tags=["paises"])


@router.get("/", response_model=PaisLista)
def get_paises(db: Session = Depends(get_db)):
    query = (
        db.query(Pais)
        .options(
            joinedload(Pais.continente),
            joinedload(Pais.idiomas),
            joinedload(Pais.actividades),
        )
        .order_by(Pais.nombre.asc())
        .all()
    )
    paises = []
    for pais in query:
        actividades_dict = [
            {"id": actividad.id, "nombre": actividad.nombre}
            for actividad in pais.actividades
        ]
        idiomas_dict = [
            {"id": idioma.id, "nombre": idioma.nombre} for idioma in pais.idiomas
        ]
        continente_dict = [
            {
                "id": pais.continente[0].id,
                "nombre": pais.continente[0].nombre,
            }
        ]

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

        paises.append(pais_dict)

    return {"paises": paises}
