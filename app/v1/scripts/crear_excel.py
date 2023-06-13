import sys
import pandas as pd
from openpyxl import Workbook
from openpyxl.utils.dataframe import dataframe_to_rows
from openpyxl.styles import Alignment
import io


def generar_excel(paises):
    """
    Esta función genera un archivo de Excel con datos de una lista de países.

    :param paises: Una lista de objetos que representan países, con atributos como nombre, capital,
    moneda, población, actividades, idiomas y continente
    """
    # Creo un dataframe con los datos de los paises
    data = []
    for pais in paises:
        actividades = ", ".join([actividad.nombre for actividad in pais.actividades])
        idiomas = ", ".join([idioma.nombre for idioma in pais.idiomas])
        continentes = ", ".join([continente.nombre for continente in pais.continente])

        pais_data = {
            "Nombre": pais.nombre,
            "Capital": pais.capital,
            "Moneda": pais.moneda,
            "Población": pais.poblacion,
            "Actividades": actividades,
            "Idiomas": idiomas,
            "Continente": continentes,
        }
        data.append(pais_data)

    df = pd.DataFrame(data)

    # Creo un excel
    wb = Workbook()
    ws = wb.active

    # cargo los datos del dataframe en el excel
    for row in dataframe_to_rows(df, index=False, header=True):
        ws.append(row)

    # Un poco de formato y blink blink
    for column in ws.columns:
        max_length = 0
        column = [cell for cell in column]
        for cell in column:
            try:
                if len(str(cell.value)) > max_length:
                    max_length = len(cell.value)
            except:
                pass
        adjusted_width = max_length + 2
        ws.column_dimensions[column[0].column_letter].width = adjusted_width

    for row in ws.iter_rows(min_row=2):
        for cell in row:
            cell.alignment = Alignment(horizontal="center", vertical="center")

    # guardar excel en memoria para enviar por correo
    buffer = io.BytesIO()
    try:
        wb.save(buffer)
    except:
        print("El archivo no se pudo guardar en memoria.")

    return buffer
