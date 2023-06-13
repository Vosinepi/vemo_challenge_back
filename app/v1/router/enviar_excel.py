import sys
from fastapi import Depends, APIRouter, BackgroundTasks
from sqlalchemy.orm import Session

sys.path.append(".")

from app.v1.utils.db import get_db
from app.v1.model.models import Pais
from app.v1.scripts.crear_excel import generar_excel
from app.v1.scripts.enviar_email import enviar_correo

router = APIRouter(prefix="/api/v1/exportar", tags=["exportar"])

"""
usar background tasks para esto
"""


# def generar_y_enviar_excel(paises, correo):
#     archivo = generar_excel(paises)
#     enviar_correo(archivo, correo)


@router.post("/")
def exportar(correo: str = None, db: Session = Depends(get_db)):
    paises = db.query(Pais).order_by(Pais.nombre).all()

    archivo = generar_excel(paises)
    enviar_correo(archivo, correo)

    return {"mensaje": "Correo enviado"}
