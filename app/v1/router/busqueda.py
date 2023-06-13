import sys
from fastapi import Depends, APIRouter
from sqlalchemy.orm import Session
from sqlalchemy import or_, func

sys.path.append(".")

from app.v1.utils.db import get_db
from app.v1.model.models import Pais, PaisContinente, Continente
from app.v1.schema.schemas import PaisLista

router = APIRouter(prefix="/api/v1/paises/busquedas", tags=["buscar"])


@router.post("/", response_model=PaisLista)
def buscar_paises(
    pais: str = None,
    capital: str = None,
    continente: str = None,
    db: Session = Depends(get_db),
):
    """
    Esta función busca países en función de los parámetros de entrada y devuelve una lista de países con
    su información respectiva.

    :param pais: Un parámetro de cadena utilizado para filtrar países por nombre
    :type pais: str
    :param capital: La capital de un país
    :type capital: str
    :param continente: El parámetro "continente" es una cadena que representa el nombre de un
    continente. Se utiliza como filtro para buscar países que pertenecen a ese continente
    :type continente: str
    :param db: db es una dependencia que proporciona una sesión de base de datos a la función. Se
    obtiene mediante la función get_db, que es una dependencia que crea una nueva sesión de base de
    datos para cada solicitud y la cierra cuando finaliza la solicitud. La sesión se utiliza para
    consultar la base de datos en busca de la información solicitada
    :type db: Session
    :return: Un diccionario con clave "paises" que contiene una lista de diccionarios, donde cada
    diccionario representa un país y su información (como id, capital, moneda, bandera, nombre,
    poblacion, actividades, continente e idiomas). Los datos devueltos se validan con el modelo
    PaisLista.
    """

    query = (
        db.query(Pais)
        .join(PaisContinente)
        .join(Continente)
        .filter(
            or_(
                func.lower(Pais.nombre).like(f"%{pais.lower()}%") if pais else False,
                func.lower(Pais.capital).like(f"%{capital.lower()}%")
                if capital
                else False,
                func.lower(Continente.nombre).like(f"%{continente.lower()}%")
                if continente
                else False,
            )
        )
        .all()
    )

    paises = []
    for pais in query:
        actividades_dict = [
            {"id": actividad.id, "nombre": actividad.nombre}
            for actividad in pais.actividades
        ]
        idiomas_dict = [
            {"id": idioma.id, "nombre": idioma.nombre} for idioma in pais.idiomas
        ]
        continente_dict = [
            {
                "id": pais.continente[0].id,
                "nombre": pais.continente[0].nombre,
            }
        ]

        pais_dict = {
            "id": pais.id,
            "capital": pais.capital,
            "moneda": pais.moneda,
            "bandera": pais.bandera,
            "nombre": pais.nombre,
            "poblacion": pais.poblacion,
            "actividades": actividades_dict,
            "continente": continente_dict,
            "idiomas": idiomas_dict,
        }

        paises.append(pais_dict)

    return {"paises": paises}
