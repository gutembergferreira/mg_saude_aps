from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from ...db.session import get_db
from ...schemas.planejamento import (
    AcaoPlanejadaCreate,
    AcaoPlanejadaOut,
    AcaoPlanejadaUpdate,
    ProblemaGUTCreate,
    ProblemaGUTOut,
    ProblemaGUTUpdate,
)
from ...services.planejamento_service import (
    atualizar_acao_planejada,
    atualizar_problema_gut,
    criar_acao_planejada,
    criar_problema_gut,
    listar_acoes_por_problema,
    listar_problemas_gut,
)

router = APIRouter()


@router.post("/problemas", response_model=ProblemaGUTOut, status_code=201)
def criar_problema(dados: ProblemaGUTCreate, db: Session = Depends(get_db)):
    return criar_problema_gut(db, dados)


@router.get("/problemas", response_model=List[ProblemaGUTOut])
def listar_problemas(
    codigo_ibge: str = Query(..., description="Código IBGE do município"),
    status: Optional[str] = Query(None, description="Status do problema"),
    db: Session = Depends(get_db),
):
    return listar_problemas_gut(db, codigo_ibge=codigo_ibge, status=status)


@router.get("/problemas/{problema_id}", response_model=ProblemaGUTOut)
def detalhe_problema(problema_id: int, db: Session = Depends(get_db)):
    from ...models.planejamento import ProblemaGUT  # lazy import to avoid circular

    problema = db.get(ProblemaGUT, problema_id)
    if not problema:
        raise HTTPException(status_code=404, detail="Problema não encontrado")
    return ProblemaGUTOut.from_orm(problema)


@router.patch("/problemas/{problema_id}", response_model=ProblemaGUTOut)
def atualizar_problema(problema_id: int, dados: ProblemaGUTUpdate, db: Session = Depends(get_db)):
    try:
        return atualizar_problema_gut(db, problema_id, dados)
    except ValueError:
        raise HTTPException(status_code=404, detail="Problema não encontrado")


@router.post("/acoes", response_model=AcaoPlanejadaOut, status_code=201)
def criar_acao(dados: AcaoPlanejadaCreate, db: Session = Depends(get_db)):
    return criar_acao_planejada(db, dados)


@router.get("/acoes/{problema_id}", response_model=List[AcaoPlanejadaOut])
def listar_acoes(problema_id: int, db: Session = Depends(get_db)):
    return listar_acoes_por_problema(db, problema_id)


@router.patch("/acoes/{acao_id}", response_model=AcaoPlanejadaOut)
def atualizar_acao(acao_id: int, dados: AcaoPlanejadaUpdate, db: Session = Depends(get_db)):
    try:
        return atualizar_acao_planejada(db, acao_id, dados)
    except ValueError:
        raise HTTPException(status_code=404, detail="Ação não encontrada")
