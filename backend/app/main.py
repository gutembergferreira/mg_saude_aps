from fastapi import FastAPI

from .api.v1 import indicadores

app = FastAPI(
    title="MG Saǧde APS",
    version="0.1.0"
)


@app.get("/health")
def health_check():
    return {"status": "ok"}


app.include_router(indicadores.router, prefix="/api/v1/indicadores", tags=["indicadores"])
