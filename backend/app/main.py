from fastapi import FastAPI

from .api.v1 import geoprocessamento, indicadores, painel_clinico, planejamento

app = FastAPI(
    title="MG Saǧde APS",
    version="0.1.0"
)


@app.get("/health")
def health_check():
    return {"status": "ok"}


app.include_router(indicadores.router, prefix="/api/v1/indicadores", tags=["indicadores"])
app.include_router(painel_clinico.router, prefix="/api/v1/painel", tags=["painel_clinico"])
app.include_router(planejamento.router, prefix="/api/v1/planejamento", tags=["planejamento"])
app.include_router(geoprocessamento.router, prefix="/api/v1/geo", tags=["geoprocessamento"])
