import sys
from smtplib import SMTP_SSL
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
from email import encoders
import logging

sys.path.append(".")

from app.v1.utils.logger import handler
from app.v1.utils.settings import EmailSettings

# Configuro el logging
logger = logging.getLogger("Envio de mail")
logger.setLevel(logging.INFO)
logger.addHandler(handler)

settings = EmailSettings()


EMAIL_HOST = settings.email_host
EMAIL_PORT = settings.email_port
EMAIL_HOST_USER = settings.email_user
EMAIL_HOST_PASSWORD = settings.email_password


server = SMTP_SSL(EMAIL_HOST)


def enviar_correo(archivo, destinatario):
    archivo.seek(0)
    # Crear mensaje de correo
    mensaje = "Adjunto encontrará el archivo con los paises del mundo"
    msg = MIMEMultipart()
    msg["From"] = EMAIL_HOST_USER
    msg["To"] = destinatario
    msg["Subject"] = "Paises del mundo"
    msg.attach(MIMEText(mensaje, "plain"))

    # Adjuntar archivo Excel
    attachment = MIMEApplication(archivo.getvalue(), _subtype="xlsx")
    attachment.add_header("Content-Disposition", "attachment", filename="paises.xlsx")
    msg.attach(attachment)

    # Enviar correo electrónico

    server.login(EMAIL_HOST_USER, EMAIL_HOST_PASSWORD)
    server.send_message(msg)

    logger.info(f"Correo enviado a {destinatario}")
