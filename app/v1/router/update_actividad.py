import sys
from fastapi import Depends, APIRouter, HTTPException, status
from sqlalchemy import func
from sqlalchemy.orm import Session, joinedload

sys.path.append(".")

from app.v1.utils.db import get_db
from app.v1.model.models import Actividad, PaisActividad, Pais
from app.v1.schema.schemas import ActividadUpdate

router = APIRouter(prefix="/api/v1/actividades", tags=["actividades"])


@router.put("/", status_code=status.HTTP_201_CREATED, response_model=ActividadUpdate)
def update_actividad(
    actividad_id: int, actividad: ActividadUpdate, db: Session = Depends(get_db)
):
    db_actividad = db.query(Actividad).filter_by(id=actividad_id).first()
    if not db_actividad:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"La actividad con id {actividad_id} no existe",
        )

    # obtener los paisea relacionados antes de la actualizacion
    id_paises_viejos = set(pais.id for pais in db_actividad.paises)

    # obtener los paises nuevos de la actualizacion
    id_paises_nuevos = set(actividad.paises_con_actividad)

    # obtener los paises que se deben eliminar
    id_paises_eliminar = id_paises_viejos - id_paises_nuevos

    # obtener los paises que se deben agregar
    id_paises_agregar = id_paises_nuevos - id_paises_viejos

    # eliminar los paises que no estan en la actualizacion
    for id_pais in id_paises_eliminar:
        db.query(PaisActividad).filter_by(
            id_pais=id_pais, id_actividad=actividad_id
        ).delete(synchronize_session=False)

    # agregar los paises que estan en la actualizacion
    # valido los paises que se van a agregar con los que ya existen en la base de datos
    paises = (
        db.query(Pais)
        .filter(
            func.lower(Pais.nombre).in_([pais.lower() for pais in id_paises_agregar])
        )
        .all()
    )

    for pais in paises:
        PaisActividad_db = PaisActividad(id_pais=pais.id, id_actividad=actividad_id)
        db.add(PaisActividad_db)

    # actualizo la actividad
    db_actividad.nombre = actividad.nombre
    db_actividad.descripcion = actividad.descripcion
    db.commit()
    db.refresh(db_actividad)

    listado_paises = [pais.nombre for pais in paises]
    actividad_response = {
        "nombre": db_actividad.nombre,
        "descripcion": db_actividad.descripcion,
        "paises_con_actividad": listado_paises,
    }
    return actividad_response
