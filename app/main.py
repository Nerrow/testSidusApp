import logging

import uvicorn
from fastapi import FastAPI

from app.api import api_router
from app.db.db_utils import (close_postgres_connection, connect_to_postgres,
                             connect_to_redis, create_db_metadata,
                             disconnect_from_redis)
from app.settings import settings
from app.utils import PrometheusMiddleware, metrics, setting_otlp

app = FastAPI()

app.add_middleware(PrometheusMiddleware, app_name=settings.app_name)
app.add_route("/metrics", metrics)
app.include_router(api_router)

setting_otlp(app, settings.app_name, settings.otlp_grpc_endpoint)


class EndpointFilter(logging.Filter):
    def filter(self, record: logging.LogRecord) -> bool:
        return record.getMessage().find("GET /metrics") == -1


logging.getLogger("uvicorn.access").addFilter(EndpointFilter())


@app.on_event("startup")
async def on_start():
    await connect_to_postgres()
    await create_db_metadata()
    await connect_to_redis()


@app.on_event("shutdown")
async def on_shutdown():
    await close_postgres_connection()
    await disconnect_from_redis()


@app.get("/healthcheck")
async def healthcheck_handler():
    return {"message": "OK"}


if __name__ == "__main__":
    log_config = uvicorn.config.LOGGING_CONFIG
    log_config["formatters"]["access"][
        "fmt"
    ] = "%(asctime)s %(levelname)s [%(name)s] [%(filename)s:%(lineno)d] [trace_id=%(otelTraceID)s span_id=%(otelSpanID)s resource.service.name=%(otelServiceName)s] - %(message)s"
    uvicorn.run(
        app, host="0.0.0.0", port=settings.app_port, workers=1, log_config=log_config
    )
