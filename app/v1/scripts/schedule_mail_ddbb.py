import sys
from apscheduler.schedulers.background import BackgroundScheduler
import logging


sys.path.append(".")

# modulos propios
from app.v1.utils.db import SessionLocal
from app.v1.utils.logger import handler
from app.v1.model.models import Pais
from app.v1.scripts.crear_excel import generar_excel
from app.v1.scripts.enviar_email import enviar_correo
from app.v1.scripts.carga_paises import cargar_datos


"""Esta clase programa una tarea para actualizar datos, generar un archivo de Excel
y enviarlo por correo electrónico a un destinatario específico."""


class ScheduleMailDdbb:
    def __init__(self):
        self.scheduler = None
        self.running = False
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.INFO)
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

    def start(self, intervalo=84600):
        # inicia la tarea programada
        if self.running == False:
            self.scheduler = BackgroundScheduler()
            self.scheduler.add_job(
                self.actualizar_enviar_correo, "interval", seconds=intervalo
            )
            self.scheduler.start()
            self.running = True
            self.logger.info(
                "Tarea programada iniciada con un intervalo de {} segundos".format(
                    intervalo
                )
            )
        else:
            self.logger.info("Tarea programada ya en funcionamiento")

    def stop(self):  # detiene la tarea programada
        if self.running:
            self.running = False
            self.scheduler.shutdown()
            self.logger.info("Tarea programada detenida")
        else:
            self.logger.info("Tarea programada ya detenida")

    def estado(self):  # devuelve el estado de la tarea programada
        if self.scheduler.running:
            return {"Estado": "En funcionamiento"}
        else:
            return {"Estado": "Detenido"}


scheduler_mail_ddbb = ScheduleMailDdbb()
