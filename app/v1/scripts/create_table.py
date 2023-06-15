from sqlalchemy import inspect, text
import sys

sys.path.append(".")

# modulos propios
from app.v1.utils.db import engine
from app.v1.model.models import Base
from app.v1.model import models


# creo las tablas
def create_table():
    inspector = inspect(engine)
    tablas_creadas = inspector.get_table_names()

    if tablas_creadas:
        inspector = inspect(engine)
        tablas_creadas = inspector.get_table_names()
        print("Tablas ya creadas creadas")
    elif not tablas_creadas:
        Base.metadata.create_all(engine)
        print("Tablas creadas")
    else:
        print("Tablas no creadas")
