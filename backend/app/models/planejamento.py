from datetime import datetime
from sqlalchemy import Column, Date, DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.orm import relationship

from ..db.base import Base


class ProblemaGUT(Base):
    __tablename__ = "app_problema_gut"

    id = Column(Integer, primary_key=True, index=True)
    id_municipio = Column(Integer, ForeignKey("dw.dim_municipio.id_municipio"), nullable=False)
    id_unidade = Column(Integer, ForeignKey("dw.dim_unidade_saude.id_unidade"), nullable=True)
    id_equipe = Column(Integer, ForeignKey("dw.dim_equipe.id_equipe"), nullable=True)
    titulo = Column(String(255), nullable=False)
    descricao = Column(Text)
    gravidade = Column(Integer, nullable=False)
    urgencia = Column(Integer, nullable=False)
    tendencia = Column(Integer, nullable=False)
    score_gut = Column(Integer, nullable=False)
    status = Column(String(20), nullable=False, default="planejado")
    data_criacao = Column(DateTime, default=datetime.utcnow, nullable=False)
    data_ultima_atualizacao = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    criado_por = Column(String(100))

    acoes = relationship("AcaoPlanejada", back_populates="problema", cascade="all, delete-orphan")


class AcaoPlanejada(Base):
    __tablename__ = "app_acao_planejada"

    id = Column(Integer, primary_key=True, index=True)
    problema_id = Column(Integer, ForeignKey("app_problema_gut.id"), nullable=False)
    descricao = Column(Text, nullable=False)
    responsavel = Column(String(100))
    data_inicio_prevista = Column(Date)
    data_fim_prevista = Column(Date)
    data_inicio_real = Column(Date)
    data_fim_real = Column(Date)
    status = Column(String(20), nullable=False, default="planejada")
    observacoes = Column(Text)

    problema = relationship("ProblemaGUT", back_populates="acoes")
