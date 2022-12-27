import aioredis
from aioredis import Redis
from redis.connection import ConnectionPool
from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession
from sqlalchemy.orm import sessionmaker


class Postgres:
    engine: AsyncEngine = None


postgres = Postgres()


async def get_postgres_session() -> AsyncSession:
    async_session = sessionmaker(
        bind=postgres.engine, class_=AsyncSession, expire_on_commit=False
    )
    async with async_session() as session:
        try:
            yield session
        finally:
            await session.close()


class RedisClient:
    conn: Redis = None


redis = RedisClient()


async def get_redis_session():
    async with redis.conn.client() as conn:
        yield conn
