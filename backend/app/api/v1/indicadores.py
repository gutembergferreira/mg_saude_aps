from fastapi import APIRouter

router = APIRouter()


@router.get("/")
def listar_indicadores_stub():
    # Stub inicial para testar estrutura
    return {"message": "Endpoint de indicadores APS - em construção"}
