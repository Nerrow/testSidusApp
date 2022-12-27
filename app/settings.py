import os

from pydantic import BaseSettings, RedisDsn, PostgresDsn


class Settings(BaseSettings):
    app_name: str = os.environ.get("APP_NAME", "app")
    app_port: int = os.environ.get("APP_PORT", 8000)
    app_workers: int = os.environ.get("APP_WORKERS", 1)
    redis_url: RedisDsn = os.environ.get("REDIS_URL", "redis://redis:6379/0")
    otlp_grpc_endpoint: str = os.environ.get("OTLP_GRPC_ENDPOINT", "http://tempo:4317")
    pg_connection_str: PostgresDsn = os.environ.get("PG_CONNECTION_STR", "postgresql+asyncpg://postgres:5432/testSidusApp")
    access_token_expire_minutes: int = 1440
    secret_key: str = os.environ.get("SECRET_KEY", "forgottentoken")
    algorithm: str = "HS256"


settings = Settings()
