from sqlalchemy import Column, Integer, String, ForeignKey, Table, MetaData
from sqlalchemy.orm import relationship
import sys

sys.path.append(".")

from app.v1.utils.db import Base

metadata = MetaData()


class Pais(Base):
    __tablename__ = "pais"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, unique=True, index=True)
    capital = Column(String, nullable=False)
    moneda = Column(String, nullable=False)
    poblacion = Column(Integer)
    bandera = Column(String, unique=True, index=True)
    # continentes enlaca a la tabla de continentes
    continente = relationship("Continente", secondary="pais_continente")
    # idiomas enlaca a la tabla de idiomas
    idiomas = relationship("Idioma", secondary="pais_idioma")
    # actividades enlaca a la tabla de actividades
    actividades = relationship("Actividad", secondary="pais_actividad")


class Continente(Base):
    __tablename__ = "continente"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, unique=True, index=True)


class Idioma(Base):
    __tablename__ = "idioma"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, unique=True, index=True)


class Actividad(Base):
    __tablename__ = "actividad"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, unique=True, index=True)


class PaisContinente(Base):
    __tablename__ = "pais_continente"

    id_pais = Column(Integer, ForeignKey("pais.id"), primary_key=True)
    id_continente = Column(Integer, ForeignKey("continente.id"), primary_key=True)


class PaisIdioma(Base):
    __tablename__ = "pais_idioma"

    id_pais = Column(Integer, ForeignKey("pais.id"), primary_key=True)
    id_idioma = Column(Integer, ForeignKey("idioma.id"), primary_key=True)


class PaisActividad(Base):
    __tablename__ = "pais_actividad"

    id_pais = Column(Integer, ForeignKey("pais.id"), primary_key=True)
    id_actividad = Column(Integer, ForeignKey("actividad.id"), primary_key=True)


# agrego extend_existing=True para que no me de error de que ya existe la tabla

pais_tabla = Table(
    "pais",
    metadata,
    Column("id", Integer, primary_key=True, index=True),
    Column("nombre", String, unique=True, index=True),
    Column("capital", String),
    Column("moneda", String),
    Column("poblacion", Integer),
    Column("bandera", String, unique=True, index=True),
    extend_existing=True,
)
