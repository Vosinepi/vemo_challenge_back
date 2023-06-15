import sys

from cachetools import TTLCache
from datetime import timedelta
from fastapi import APIRouter
from fastapi_cache import FastAPICache
from fastapi_cache.backends.memcached import MemcachedBackend

sys.path.append(".")

# modulos propios
from v1.scripts.create_table import create_table
from app.v1.scripts.carga_paises import cargar_datos
from app.v1.scripts.schedule_mail_ddbb import scheduler_mail_ddbb as scheduler
from v1.model.models import *

# crear cache
cache = TTLCache(maxsize=1000, ttl=timedelta(minutes=5))
backend = MemcachedBackend("memcached")

router = APIRouter(tags=["Crear_Cargar"])


@router.on_event("startup")
async def startup_event():
    create_table()
    cargar_datos()

    # Configuración de la capa de caché
    FastAPICache.init(backend, prefix="fastapi-cache")

    # tarea de actualizacion diaria de datos y envio de mail
    scheduler.start()
