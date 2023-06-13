import sys
from fastapi import Depends, APIRouter, Response
from fastapi.responses import FileResponse
from starlette.responses import StreamingResponse
from io import BytesIO
from sqlalchemy.orm import Session

sys.path.append(".")

from app.v1.utils.db import get_db
from app.v1.model.models import Pais

from app.v1.scripts.crear_excel import generar_excel


router = APIRouter(prefix="/api/v1/descargas", tags=["descarga"])


@router.get("/")
def exportar(response: Response, db: Session = Depends(get_db)):
    paises = db.query(Pais).order_by(Pais.nombre).all()

    # Generar el archivo
    archivo = generar_excel(paises)
    archivo.seek(0)

    # Descargar el archivo mediante StreamingResponse
    descarga = StreamingResponse(
        BytesIO(archivo.getvalue()),
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
    )
    descarga.headers["Content-Disposition"] = 'attachment; filename="paises.xlsx"'

    return descarga
