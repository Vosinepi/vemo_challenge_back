import requests
import sys
import logging

sys.path.append(".")

# modulos propios
from app.v1.utils.db import SessionLocal
from app.v1.utils.logger import handler
from app.v1.model.models import (
    Pais,
    Continente,
    Idioma,
    PaisContinente,
    PaisIdioma,
)

# Configuro el logging
logger = logging.getLogger("Carga de datos")
logger.setLevel(logging.INFO)
logger.addHandler(handler)


def cargar_datos():
    # apí de consulta
    api = "https://restcountries.com/v3.1/all"

    # hacemos la petición
    try:
        response = requests.get(api)
    except requests.exceptions.RequestException as e:
        print("Error de conexión")
        sys.exit(1)

    # obtenemos los datos
    data = response.json()

    # creamos la sesión
    db = SessionLocal()

    # cargamos los paises
    for pais_data in data:
        pais = pais_data["name"]["common"]
        print(pais)
        try:
            capital = pais_data["capital"][0]

        except:
            print("Sin capital")
            capital = "Sin Capital"
        try:
            moneda = (next(iter(pais_data["currencies"].values())))["name"]

        except:
            print("Sin moneda")
            moneda = "Sin Moneda"
        poblacion = pais_data["population"]

        flag = pais_data.get("flags")["png"]

        existe_registro = db.query(Pais).filter(Pais.nombre == pais).first()
        if existe_registro:
            print("El registro ya existe")

        else:
            pais = Pais(
                nombre=pais,
                capital=capital,
                moneda=moneda,
                poblacion=poblacion,
                bandera=flag,
            )
            db.add(pais)
    db.commit()

    for pais_data in data:
        pais = pais_data["name"]["common"]
        # creamos registro de los continentes e idiomas
        continentes = pais_data.get("continents", [])
        print(continentes)
        idiomas = pais_data.get("languages", {}).values()
        print(idiomas)
        pais_nombre = db.query(Pais).filter(Pais.nombre == pais).first()

        for continente_nombre in continentes:
            continente = (
                db.query(Continente)
                .filter(Continente.nombre == continente_nombre)
                .first()
            )
            if not continente:
                continente = Continente(nombre=continente_nombre)
                db.add(continente)

                db.commit()

            # creo relacion continente pais
            pais_id = db.query(Pais).filter(Pais.nombre == pais).first()

            # si la relacion ya existe no la creo
            existe_relacion = (
                db.query(PaisContinente)
                .filter(PaisContinente.id_pais == pais_id.id)
                .filter(PaisContinente.id_continente == continente.id)
                .first()
            )
            if existe_relacion:
                print("La relacion ya existe")
            else:
                pais_continente = PaisContinente(
                    id_pais=pais_id.id, id_continente=continente.id
                )
                db.add(pais_continente)
                db.commit()

        for idioma_nombre in idiomas:
            idioma = db.query(Idioma).filter(Idioma.nombre == idioma_nombre).first()
            if not idioma:
                idioma = Idioma(nombre=idioma_nombre)
                db.add(idioma)

                db.commit()

            # creo relacion idioma pais

            # si la relacion ya existe no la creo
            existe_relacion = (
                db.query(PaisIdioma)
                .filter(PaisIdioma.id_pais == pais_id.id)
                .filter(PaisIdioma.id_idioma == idioma.id)
                .first()
            )
            if existe_relacion:
                print("La relacion ya existe")
            else:
                pais_idioma = PaisIdioma(id_pais=pais_id.id, id_idioma=idioma.id)
                db.add(pais_idioma)
                db.commit()

    db.commit()
    db.close()
    logger.info("Datos cargados y actulizacdos")


if __name__ == "__main__":
    cargar_datos()
