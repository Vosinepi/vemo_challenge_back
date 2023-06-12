from sqlalchemy import inspect, text

import sys

sys.path.append(".")

from app.v1.utils import db

# from utils.db import Base, engine
from app.v1.model import models


# creo las tablas
def create_table():
    db.Base.metadata.create_all(db.engine)

    inspector = inspect(db.engine)
    tablas_creadas = inspector.get_table_names()

    if tablas_creadas:
        print("Tablas creadas\n")

    else:
        print("Tablas no creadas")


create_table()
