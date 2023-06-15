import sys
from fastapi import Depends, APIRouter, HTTPException, status

from sqlalchemy.orm import Session

from fastapi_cache.backends.memcached import MemcachedBackend
from fastapi_cache import FastAPICache
from cachetools import TTLCache
from datetime import timedelta

sys.path.append(".")

# modulos propios
from app.v1.utils.db import get_db
from app.v1.model.models import Actividad

# crear nuevo cache
cache = TTLCache(maxsize=1000, ttl=timedelta(minutes=5))
backend = MemcachedBackend(cache)


router = APIRouter(prefix="/api/v1/actividades/{id}", tags=["actividades"])


@router.delete("/", status_code=status.HTTP_200_OK)
def delete_actividades(
    id: int,
    db: Session = Depends(get_db),
):
    # busco la actividad
    actividad = db.query(Actividad).filter_by(id=id).first()
    if actividad:
        db.delete(actividad)
        db.commit()
        return {"detail": f"La actividad {actividad.nombre} ha sido borrada"}
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"La actividad con id {id} no existe",
        )

    # Reseteo la capa de caché creando una nueva instancia de la misma
    FastAPICache.init(backend, prefix="fastapi-cache")
