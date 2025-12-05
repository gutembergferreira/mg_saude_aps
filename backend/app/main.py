from time import perf_counter
from typing import Dict

from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from loguru import logger
from sqlalchemy import text
from starlette.responses import PlainTextResponse

from .api.v1 import geoprocessamento, indicadores, painel_clinico, planejamento
from .core.config import get_settings
from .core.logging import configure_logging
from .db.session import SessionLocal
from .web_ui import routes as web_routes

configure_logging()
settings = get_settings()
app = FastAPI(title="MG Saúde APS", version="0.1.0")

requests_total = 0
errors_total = 0


@app.middleware("http")
async def log_requests(request: Request, call_next):
    global requests_total, errors_total
    start = perf_counter()
    response = await call_next(request)
    duration_ms = (perf_counter() - start) * 1000
    requests_total += 1
    if response.status_code >= 500:
        errors_total += 1
    logger.info(
        "[REQUEST] method={method} path={path} status={status} duration_ms={duration:.2f}",
        method=request.method,
        path=request.url.path,
        status=response.status_code,
        duration=duration_ms,
    )
    return response


@app.get("/health")
def health_check():
    return {"status": "ok"}


@app.get("/health/details")
def health_details():
    db_status: Dict[str, object] = {"status": "ok", "latency_ms": None}
    try:
        start = perf_counter()
        with SessionLocal() as session:
            session.execute(text("SELECT 1"))
        db_status["latency_ms"] = (perf_counter() - start) * 1000
    except Exception as exc:  # pragma: no cover - defensive
        db_status = {"status": "error", "error": str(exc)}
        return {"status": "degraded", "app": {"name": settings.APP_NAME, "version": app.version}, "database": db_status}

    return {
        "status": "ok",
        "app": {"name": settings.APP_NAME, "version": app.version},
        "database": db_status,
    }


@app.get("/metrics")
def metrics():
    body = f"mg_saude_requests_total {requests_total}\nmg_saude_errors_total {errors_total}\n"
    return PlainTextResponse(body, media_type="text/plain")


app.include_router(indicadores.router, prefix="/api/v1/indicadores", tags=["indicadores"])
app.include_router(painel_clinico.router, prefix="/api/v1/painel", tags=["painel_clinico"])
app.include_router(planejamento.router, prefix="/api/v1/planejamento", tags=["planejamento"])
app.include_router(geoprocessamento.router, prefix="/api/v1/geo", tags=["geoprocessamento"])
app.include_router(web_routes.router, tags=["web"])
app.mount("/static", StaticFiles(directory="backend/app/static"), name="static")
