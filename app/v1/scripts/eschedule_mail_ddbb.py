import sys

sys.path.append(".")

from app.v1.utils.db import SessionLocal
from app.v1.model.models import Pais
from app.v1.scripts.crear_excel import generar_excel
from app.v1.scripts.enviar_email import enviar_correo
from app.v1.scripts.carga_paises import cargar_datos


def actualizar_enviar_correo():
    """
    Esta función actualiza los datos, genera un archivo de Excel con los datos actualizados y lo envía
    por correo electrónico a un destinatario específico.
    :return: a dictionary with the message "Actualizacion diario en funcionamiento".
    """
    db = SessionLocal()
    correo = "ismaelpiovani@gmail.com"
    cargar_datos()

    paises = db.query(Pais).order_by(Pais.nombre).all()

    archivo = generar_excel(paises)
    enviar_correo(archivo, correo)

    return {"Actualizacion diario en funcionamiento"}
