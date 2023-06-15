from cachetools import TTLCache
from datetime import timedelta
from fastapi import APIRouter
from fastapi_cache import FastAPICache
from fastapi_cache.backends.memcached import MemcachedBackend


async def reset_cache():
    await FastAPICache.clear()
    print("Cache reseteada")


cache = TTLCache(maxsize=1000, ttl=timedelta(minutes=5))
backend = MemcachedBackend("memcached")


def reset(back):
    FastAPICache.init(back)


reset(backend)
