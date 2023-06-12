from fastapi import Depends, APIRouter
from sqlalchemy.orm import Session
from sqlalchemy import or_, func

from v1.utils.db import get_db
from v1.model.models import Pais, PaisContinente, Continente
from v1.schema.schemas import PaisLista

router = APIRouter(prefix="/paises/buscar", tags=["buscar"])


@router.get("/", response_model=PaisLista)
def buscar_paises(
    pais: str = None,
    capital: str = None,
    continente: str = None,
    db: Session = Depends(get_db),
):
    query = (
        db.query(Pais)
        .join(PaisContinente)
        .join(Continente)
        .filter(
            or_(
                func.lower(Pais.nombre).like(f"%{pais.lower()}%") if pais else False,
                func.lower(Pais.capital).like(f"%{capital.lower()}%")
                if capital
                else False,
                func.lower(Continente.nombre).like(f"%{continente.lower()}%")
                if continente
                else False,
            )
        )
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
