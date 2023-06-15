from pydantic import BaseModel, Field
from typing import List, Optional


class IdiomaBase(BaseModel):
    nombre: str


class ContinenteBase(BaseModel):
    nombre: str


class ActividadBase(BaseModel):
    nombre: str
    descripcion: Optional[str] = "Sin descripcion"
    paises_con_actividad: Optional[List[str]] = None

    class Config:
        orm_mode = True


class PaisBase(BaseModel):
    nombre: str
    capital: str
    moneda: str = "Sin moneda"
    poblacion: int
    bandera: str
    continente: List[ContinenteBase]
    idiomas: List[IdiomaBase]
    actividades: Optional[List[ActividadBase]] = None

    class Config:
        orm_mode = True


class PaisId(PaisBase):
    id: int


class PaisLista(BaseModel):
    paises: List[PaisBase]


class PaisDetalle(BaseModel):
    pais: List[PaisBase]


class ActividadCreate(ActividadBase):
    pass


class ActividadUpdate(ActividadBase):
    pass


class ActividadView(ActividadBase):
    id: int

    class Config:
        orm_mode = True
