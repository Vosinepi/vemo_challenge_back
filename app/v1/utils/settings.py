import os

from pydantic import BaseSettings
from dotenv import load_dotenv

load_dotenv()


# La clase define la configuración para una conexión de base de datos y genera un error si no se
# establece el nombre de la base de datos.
class Settings(BaseSettings):
    db_name: str = os.getenv("DB_NAME", "")
    db_user: str = os.getenv("DB_USER", "")
    db_password: str = os.getenv("DB_PASS", "")
    db_host: str = os.getenv("DB_HOST", "")
    db_port: str = os.getenv("DB_PORT", "")

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        if self.db_name is None:
            raise ValueError("DB_NAME is not set")


# La clase `EmailSettings` define la configuración del correo electrónico y genera un error si el
# usuario del correo electrónico no está configurado.
class EmailSettings(BaseSettings):
    email_user: str = os.getenv("EMAIL_HOST_USER", "")
    email_password: str = os.getenv("EMAIL_HOST_PASSWORD", "")
    email_host: str = os.getenv("EMAIL_HOST", "")
    email_port: str = os.getenv("EMAIL_PORT", "")

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        if self.email_user is None:
            raise ValueError("EMAIL_USER is not set")
