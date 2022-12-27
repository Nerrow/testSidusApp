import json
from datetime import datetime
from uuid import UUID

from aioredis import Redis


def custom_serializer(obj):
    if isinstance(obj, UUID):
        return str(obj)
    if isinstance(obj, datetime):
        return obj.isoformat()


def datetime_parser(dct):
    for k, v in dct.items():
        if isinstance(v, str) and v.endswith("+00:00"):
            try:
                dct[k] = datetime.fromisoformat(v)
            except:
                pass
    return dct


async def get_cache(redis_conn: Redis, key: str):
    cached_data = await redis_conn.get(key)

    if cached_data:
        print(json.loads(cached_data, object_hook=datetime_parser))
        return json.loads(cached_data, object_hook=datetime_parser)
    return None


async def set_cache(redis_conn: Redis, key: str, data: dict):
    print(json.dumps(data, indent=4, default=custom_serializer))
    await redis_conn.set(
        key,
        json.dumps(data, default=custom_serializer),
        ex=86400,
    )


async def invalidate_cache(redis_conn: Redis, key: str):
    await redis_conn.delete(str(key))
