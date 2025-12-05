from typing import List, Optional

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from ...db.session import get_db
from ...schemas.painel_clinico import CriancaOut, GestanteOut
from ...services.painel_clinico_service import listar_criancas_municipio, listar_gestantes_municipio

router = APIRouter()


@router.get(
    "/gestantes/{codigo_ibge_municipio}",
    response_model=List[GestanteOut],
    summary="Lista gestantes com atendimentos nos últimos 12 meses",
)
def listar_gestantes(
    codigo_ibge_municipio: str,
    unidade: Optional[str] = Query(None, description="Código CNES da unidade"),
    equipe: Optional[str] = Query(None, description="Código da equipe"),
    db: Session = Depends(get_db),
):
    return listar_gestantes_municipio(db, codigo_ibge=codigo_ibge_municipio, unidade=unidade, equipe=equipe)


@router.get(
    "/criancas/{codigo_ibge_municipio}",
    response_model=List[CriancaOut],
    summary="Lista crianças com atendimentos nos últimos 12 meses",
)
def listar_criancas(
    codigo_ibge_municipio: str,
    unidade: Optional[str] = Query(None, description="Código CNES da unidade"),
    equipe: Optional[str] = Query(None, description="Código da equipe"),
    faixa_etaria: Optional[str] = Query(None, description="Faixa etária (ex.: 0-1, 1-4)"),
    db: Session = Depends(get_db),
):
    return listar_criancas_municipio(
        db, codigo_ibge=codigo_ibge_municipio, unidade=unidade, equipe=equipe, faixa_etaria=faixa_etaria
    )
