import logging

import aioredis
from sqlalchemy.ext.asyncio import create_async_engine

from app.db.db import postgres, redis
from app.models.core import Base
from app.settings import settings


async def connect_to_postgres():
    logging.info("Connecting to postgres...")
    postgres.engine = create_async_engine(
        settings.pg_connection_str, echo=True, future=True
    )
    logging.info("Postgres connected")


async def create_db_metadata():
    logging.info("Setting up metadata...")
    async with postgres.engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    logging.info("Metadata created successfully")


async def close_postgres_connection():
    logging.info("Closing postgres connection...")
    await postgres.engine.dispose()
    logging.info("Postgres connection closed")


async def connect_to_redis():
    logging.info(f"Connecting to redis...")
    redis.conn = aioredis.from_url(
        settings.redis_url, encoding="utf-8", decode_responses=True
    )
    logging.info(f"Connection to redis set successfully")


async def disconnect_from_redis():
    logging.info(f"Disconnecting from redis...")
    await redis.conn.close()
    logging.info(f"Disconnecting from redis successfully")
