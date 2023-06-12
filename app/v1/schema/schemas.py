from pydantic import BaseModel, Field
from typing import List, Optional


class IdiomaBase(BaseModel):
    nombre: str


class ContinenteBase(BaseModel):
    nombre: str


class ActividadBase(BaseModel):
    nombre: str


class PaisBase(BaseModel):
    nombre: str
    capital: str
    moneda: str = "Sin moneda"
    poblacion: int
    bandera: str
    continente: List[ContinenteBase]
    idiomas: List[IdiomaBase]
    actividades: Optional[List[ActividadBase]]

    class Config:
        orm_mode = True


class PaisLista(BaseModel):
    paises: List[PaisBase]


class PaisDetalle(BaseModel):
    pais: List[PaisBase]


class ActividadCreate(ActividadBase):
    pass


class ActividadUpdate(ActividadBase):
    pass


class Actividad(ActividadBase):
    id: int

    class Config:
        orm_mode = True
