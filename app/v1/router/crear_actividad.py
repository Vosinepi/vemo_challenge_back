import sys
from fastapi import Depends, APIRouter, HTTPException, status
from sqlalchemy import func
from sqlalchemy.orm import Session, joinedload

sys.path.append(".")

from app.v1.utils.db import get_db
from app.v1.model.models import Actividad, PaisActividad, Pais
from app.v1.schema.schemas import ActividadCreate

router = APIRouter(prefix="/api/v1/crear_actividades", tags=["paises"])


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=ActividadCreate)
def crear_actividades(
    actividad: ActividadCreate,
    db: Session = Depends(get_db),
):
    db_actividad = Actividad(
        nombre=actividad.nombre,
        descripcion=actividad.descripcion,
    )
    db.add(db_actividad)
    db.commit()
    db.refresh(db_actividad)

    # creo la relacion entre paises y actividades

    # obtengo los paises de la base de datos no importa si es mayuscula o minuscula
    paises = (
        db.query(Pais)
        .filter(
            func.lower(Pais.nombre).in_(
                [pais.lower() for pais in actividad.paises_con_actividad]
            )
        )
        .all()
    )

    for pais in paises:
        existe_relacion = (
            db.query(PaisActividad)
            .filter_by(id_pais=pais.id, id_actividad=db_actividad.id)
            .first()
        )
        if existe_relacion:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"La actividad {actividad.nombre} ya existe en el pais {pais.nombre}",
            )
        else:
            db_pais_actividad = PaisActividad(
                id_pais=pais.id,
                id_actividad=db_actividad.id,
            )
            db.add(db_pais_actividad)

    db.commit()

    listado_paises = [pais.nombre for pais in paises]
    actividad_response = {
        "nombre": db_actividad.nombre,
        "descripcion": db_actividad.descripcion,
        "paises_con_actividad": listado_paises,
    }
    return actividad_response
