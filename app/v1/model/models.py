from sqlalchemy import Column, Integer, String, ForeignKey, Table, MetaData
from sqlalchemy.orm import relationship

import sys

sys.path.append(".")


from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

metadata = MetaData()


# modelos de la base de datos
class Pais(Base):
    __tablename__ = "pais"
    __table_args__ = {"extend_existing": True}

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
    __table_args__ = {"extend_existing": True}

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, unique=True, index=True)


class Idioma(Base):
    __tablename__ = "idioma"
    __table_args__ = {"extend_existing": True}

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, unique=True, index=True)


class Actividad(Base):
    __tablename__ = "actividad"
    __table_args__ = {"extend_existing": True}

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, unique=True, index=True)
    descripcion = Column(String, nullable=False)
    # paises enlaca a la tabla de paises
    paises = relationship("Pais", secondary="pais_actividad")


class PaisContinente(Base):
    __tablename__ = "pais_continente"
    __table_args__ = {"extend_existing": True}

    id_pais = Column(Integer, ForeignKey("pais.id"), primary_key=True)
    id_continente = Column(Integer, ForeignKey("continente.id"), primary_key=True)


class PaisIdioma(Base):
    __tablename__ = "pais_idioma"
    __table_args__ = {"extend_existing": True}

    id_pais = Column(Integer, ForeignKey("pais.id"), primary_key=True)
    id_idioma = Column(Integer, ForeignKey("idioma.id"), primary_key=True)


class PaisActividad(Base):
    __tablename__ = "pais_actividad"
    __table_args__ = {"extend_existing": True}

    id_pais = Column(Integer, ForeignKey("pais.id"), primary_key=True)
    id_actividad = Column(Integer, ForeignKey("actividad.id"), primary_key=True)
