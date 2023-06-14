import sys
from apscheduler.schedulers.background import BackgroundScheduler
import logging

sys.path.append(".")

from app.v1.utils.db import SessionLocal
from app.v1.model.models import Pais
from app.v1.scripts.crear_excel import generar_excel
from app.v1.scripts.enviar_email import enviar_correo
from app.v1.scripts.carga_paises import cargar_datos


"""Esta clase que programa una tarea para actualizar datos, generar un archivo de Excel
y enviarlo por correo electrónico a un destinatario específico."""


class ScheduleMailDdbb:
    def __init__(self):
        self.scheduler = None
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.INFO)

        # Configuro el logging
        handler = logging.FileHandler("app/v1/logs/schedule_mail_ddbb.log")
        formatter = logging.Formatter(
            "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        )
        handler.setFormatter(formatter)
        self.logger.addHandler(handler)

    def actualizar_enviar_correo(self):
        """
        Esta función actualiza los datos, genera un archivo de Excel con los datos actualizados y lo envía
        por correo electrónico a un destinatario específico.
        :return: a dictionary with the message "Actualizacion diario en funcionamiento".
        """
        db = SessionLocal()
        correo = "ismaelpiovani@gmail.com"
        try:
            cargar_datos()
            self.logger.info("Datos cargados correctamente")
        except Exception as e:
            self.logger.error("Error al cargar los datos: {}".format(e))

        paises = db.query(Pais).order_by(Pais.nombre).all()
        try:
            archivo = generar_excel(paises)
            enviar_correo(archivo, correo)
            self.logger.info("Correo enviado correctamente")
        except Exception as e:
            self.logger.error("Error al enviar el correo: {}".format(e))

    def start(self, intervalo=84600):  # inicia la tarea programada
        self.scheduler = BackgroundScheduler()
        self.scheduler.add_job(
            self.actualizar_enviar_correo, "interval", seconds=intervalo
        )
        self.scheduler.start()
        self.logger.info(
            "Tarea programada iniciada con un intervalo de {} segundos".format(
                intervalo
            )
        )

    def stop(self):  # detiene la tarea programada
        if self.scheduler and self.scheduler.running:
            self.scheduler.shutdown()
            self.logger.info("Tarea programada detenida")

    def estado(self):  # devuelve el estado de la tarea programada
        if self.scheduler and self.scheduler.running:
            return {"Estado": "En funcionamiento"}
        else:
            return {"Estado": "Detenido"}


scheduler_mail_ddbb = ScheduleMailDdbb()
