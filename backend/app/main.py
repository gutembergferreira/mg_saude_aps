from fastapi import FastAPI

app = FastAPI(
    title="MG Saúde APS",
    version="0.1.0"
)

@app.get("/health")
def health_check():
    return {"status": "ok"}

# futuras rotas:
# from .api.v1 import indicadores
# app.include_router(indicadores.router, prefix="/api/v1/indicadores", tags=["indicadores"])
