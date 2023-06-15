import sys
from fastapi import Depends, APIRouter
from sqlalchemy.orm import Session

sys.path.append(".")

from app.v1.utils.db import get_db
from app.v1.model.models import Pais
from app.v1.scripts.crear_excel import generar_excel
from app.v1.scripts.enviar_email import enviar_correo

router = APIRouter(prefix="/api/v1/exportar", tags=["utilidades"])


@router.get("/")
def enviar_mail(correo: str = None, db: Session = Depends(get_db)):
    paises = db.query(Pais).order_by(Pais.nombre).all()

    archivo = generar_excel(paises)  # Genera el excel
    try:
        enviar_correo(archivo, correo)
    except Exception as e:
        return {"mensaje": "Error al enviar el correo", "error": str(e)}

    return {"mensaje": "Correo enviado"}
