from datetime import datetime
from typing import List, Optional

from sqlalchemy import select
from sqlalchemy.orm import Session

from ..models.dw import DimMunicipio
from ..models.planejamento import AcaoPlanejada, ProblemaGUT
from ..schemas.planejamento import (
    AcaoPlanejadaCreate,
    AcaoPlanejadaOut,
    AcaoPlanejadaUpdate,
    ProblemaGUTCreate,
    ProblemaGUTOut,
    ProblemaGUTUpdate,
)


def _recalcular_score(gravidade: int, urgencia: int, tendencia: int) -> int:
    return gravidade * urgencia * tendencia


def _get_id_municipio(db: Session, codigo_ibge: str) -> Optional[int]:
    row = db.execute(select(DimMunicipio.id_municipio).where(DimMunicipio.codigo_ibge == codigo_ibge)).first()
    return row[0] if row else None


def criar_problema_gut(db: Session, dados: ProblemaGUTCreate) -> ProblemaGUTOut:
    score = _recalcular_score(dados.gravidade, dados.urgencia, dados.tendencia)
    problema = ProblemaGUT(
        **dados.dict(),
        score_gut=score,
    )
    db.add(problema)
    db.commit()
    db.refresh(problema)
    return ProblemaGUTOut.from_orm(problema)


def atualizar_problema_gut(db: Session, problema_id: int, dados: ProblemaGUTUpdate) -> ProblemaGUTOut:
    problema = db.get(ProblemaGUT, problema_id)
    if not problema:
        raise ValueError("Problema não encontrado")

    update_data = dados.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(problema, field, value)

    if any(k in update_data for k in ("gravidade", "urgencia", "tendencia")):
        problema.score_gut = _recalcular_score(
            problema.gravidade,
            problema.urgencia,
            problema.tendencia,
        )
    problema.data_ultima_atualizacao = datetime.utcnow()

    db.commit()
    db.refresh(problema)
    return ProblemaGUTOut.from_orm(problema)


def listar_problemas_gut(db: Session, codigo_ibge: str, status: Optional[str] = None) -> List[ProblemaGUTOut]:
    query = db.query(ProblemaGUT).join(DimMunicipio, DimMunicipio.id_municipio == ProblemaGUT.id_municipio)
    query = query.filter(DimMunicipio.codigo_ibge == codigo_ibge)
    if status:
        query = query.filter(ProblemaGUT.status == status)
    results = query.order_by(ProblemaGUT.score_gut.desc(), ProblemaGUT.data_criacao).all()
    return [ProblemaGUTOut.from_orm(p) for p in results]


def criar_acao_planejada(db: Session, dados: AcaoPlanejadaCreate) -> AcaoPlanejadaOut:
    acao = AcaoPlanejada(**dados.dict())
    db.add(acao)
    db.commit()
    db.refresh(acao)
    return AcaoPlanejadaOut.from_orm(acao)


def atualizar_acao_planejada(db: Session, acao_id: int, dados: AcaoPlanejadaUpdate) -> AcaoPlanejadaOut:
    acao = db.get(AcaoPlanejada, acao_id)
    if not acao:
        raise ValueError("Ação não encontrada")
    update_data = dados.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(acao, field, value)
    db.commit()
    db.refresh(acao)
    return AcaoPlanejadaOut.from_orm(acao)


def listar_acoes_por_problema(db: Session, problema_id: int) -> List[AcaoPlanejadaOut]:
    results = db.query(AcaoPlanejada).filter(AcaoPlanejada.problema_id == problema_id).all()
    return [AcaoPlanejadaOut.from_orm(a) for a in results]
