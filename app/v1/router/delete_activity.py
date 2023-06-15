import sys
from fastapi import Depends, APIRouter, HTTPException, status
from sqlalchemy import func
from sqlalchemy.orm import Session, joinedload

sys.path.append(".")

# modulos propios
from app.v1.utils.db import get_db
from app.v1.model.models import Actividad


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
