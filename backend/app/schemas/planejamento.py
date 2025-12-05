from datetime import date, datetime
from typing import Optional

from pydantic import BaseModel, Field


class ProblemaGUTBase(BaseModel):
    id_municipio: int
    id_unidade: Optional[int] = None
    id_equipe: Optional[int] = None
    titulo: str
    descricao: Optional[str] = None
    gravidade: int = Field(..., ge=1, le=5)
    urgencia: int = Field(..., ge=1, le=5)
    tendencia: int = Field(..., ge=1, le=5)
    status: Optional[str] = "planejado"
    criado_por: Optional[str] = None


class ProblemaGUTCreate(ProblemaGUTBase):
    pass


class ProblemaGUTUpdate(BaseModel):
    titulo: Optional[str] = None
    descricao: Optional[str] = None
    gravidade: Optional[int] = Field(None, ge=1, le=5)
    urgencia: Optional[int] = Field(None, ge=1, le=5)
    tendencia: Optional[int] = Field(None, ge=1, le=5)
    status: Optional[str] = None
    id_unidade: Optional[int] = None
    id_equipe: Optional[int] = None
    criado_por: Optional[str] = None


class ProblemaGUTOut(BaseModel):
    id: int
    id_municipio: int
    id_unidade: Optional[int]
    id_equipe: Optional[int]
    titulo: str
    descricao: Optional[str]
    gravidade: int
    urgencia: int
    tendencia: int
    score_gut: int
    status: str
    data_criacao: datetime
    data_ultima_atualizacao: datetime
    criado_por: Optional[str]

    class Config:
        orm_mode = True


class AcaoPlanejadaBase(BaseModel):
    problema_id: int
    descricao: str
    responsavel: Optional[str] = None
    data_inicio_prevista: Optional[date] = None
    data_fim_prevista: Optional[date] = None
    data_inicio_real: Optional[date] = None
    data_fim_real: Optional[date] = None
    status: Optional[str] = "planejada"
    observacoes: Optional[str] = None


class AcaoPlanejadaCreate(AcaoPlanejadaBase):
    pass


class AcaoPlanejadaUpdate(BaseModel):
    descricao: Optional[str] = None
    responsavel: Optional[str] = None
    data_inicio_prevista: Optional[date] = None
    data_fim_prevista: Optional[date] = None
    data_inicio_real: Optional[date] = None
    data_fim_real: Optional[date] = None
    status: Optional[str] = None
    observacoes: Optional[str] = None


class AcaoPlanejadaOut(BaseModel):
    id: int
    problema_id: int
    descricao: str
    responsavel: Optional[str]
    data_inicio_prevista: Optional[date]
    data_fim_prevista: Optional[date]
    data_inicio_real: Optional[date]
    data_fim_real: Optional[date]
    status: str
    observacoes: Optional[str]

    class Config:
        orm_mode = True
