from sqlalchemy import text

import sys


sys.path.append(".")

from app.v1.utils import db


session = db.SessionLocal()

# elimino las tablas

stmt = text(
    "DROP TABLE IF EXISTS pais_continente, pais_idioma, pais_actividad, pais, continente, idioma, actividad"
)
session.execute(stmt)

session.commit()

session.close()
