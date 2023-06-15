import sys
from fastapi import Depends, APIRouter, status
from sqlalchemy.orm import Session, joinedload

# Decorador para cachear la respuesta de la función
from fastapi_cache.decorator import cache

sys.path.append(".")

from app.v1.utils.db import get_db
from app.v1.model.models import Actividad
from app.v1.schema.schemas import ActividadView

router = APIRouter(prefix="/api/v1/actividades", tags=["actividades"])


@router.get("/", status_code=status.HTTP_200_OK, response_model=list[ActividadView])
@cache(expire=3600)
def get_actividades(db: Session = Depends(get_db)):
    actividades = (
        db.query(Actividad)
        .options(joinedload(Actividad.paises))
        .order_by(Actividad.nombre)
        .all()
    )

    actividades_view = []
    for actividad in actividades:
        paises = [
            pais.nombre for pais in actividad.paises
        ]  # Obtener los nombres de los países
        actividad_view = ActividadView(
            id=actividad.id,
            nombre=actividad.nombre,
            descripcion=actividad.descripcion,
            paises_con_actividad=paises,
        )
        actividades_view.append(actividad_view)

    return actividades_view
