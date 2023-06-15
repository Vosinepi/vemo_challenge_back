import sys
from fastapi import Depends, APIRouter
from sqlalchemy.orm import Session
from sqlalchemy import or_, func

# Decorador para cachear la respuesta de la función
from fastapi_cache.decorator import cache

sys.path.append(".")


from app.v1.utils.db import get_db
from app.v1.model.models import Pais, PaisContinente, Continente
from app.v1.schema.schemas import PaisLista


router = APIRouter(prefix="/api/v1/paises", tags=["paises"])


@router.get("/", response_model=PaisLista)
@cache(expire=3600)
def buscar_paises(
    pais: str = None,
    capital: str = None,
    continente: str = None,
    db: Session = Depends(get_db),
):
    print("Ejecutando la función buscar_paises")
    if pais or capital or continente:
        query = (
            db.query(Pais)
            .join(PaisContinente)
            .join(Continente)
            .filter(
                or_(
                    func.lower(Pais.nombre).like(f"%{pais.lower()}%")
                    if pais
                    else False,
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
    else:
        query = db.query(Pais).order_by(Pais.nombre.asc()).all()

    paises = []
    for pais in query:
        actividades_dict = [
            {
                "id": actividad.id,
                "nombre": actividad.nombre,
                "descripcion": actividad.descripcion,
                "paises_con_actividad": [pais.nombre for pais in actividad.paises],
            }
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
