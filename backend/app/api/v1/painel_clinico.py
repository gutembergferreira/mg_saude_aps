from typing import List, Optional

from fastapi import APIRouter, Depends, Query, Request
from sqlalchemy.orm import Session

from ...core.security import ensure_user_can_access_municipio, get_current_user
from ...db.session import get_db
from ...models.app import Usuario
from ...schemas.painel_clinico import CriancaOut, GestanteOut
from ...services.auditoria_service import log_audit_access
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
    request: Request = None,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user),
):
    ensure_user_can_access_municipio(current_user, codigo_ibge_municipio, db)
    result = listar_gestantes_municipio(db, codigo_ibge=codigo_ibge_municipio, unidade=unidade, equipe=equipe)
    log_audit_access(db, request, current_user, "acesso ao painel de gestantes", sucesso=True)
    return result


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
    request: Request = None,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user),
):
    ensure_user_can_access_municipio(current_user, codigo_ibge_municipio, db)
    result = listar_criancas_municipio(
        db, codigo_ibge=codigo_ibge_municipio, unidade=unidade, equipe=equipe, faixa_etaria=faixa_etaria
    )
    log_audit_access(db, request, current_user, "acesso ao painel de criancas", sucesso=True)
    return result
