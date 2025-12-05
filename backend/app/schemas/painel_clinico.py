from datetime import date
from typing import Optional

from pydantic import BaseModel, validator

from ..core.privacy import mask_hash_identificador


class GestanteOut(BaseModel):
    id_paciente: int
    hash_identificador: Optional[str]
    municipio: str
    codigo_ibge: str
    unidade: Optional[str]
    codigo_unidade: Optional[str]
    equipe: Optional[str]
    codigo_equipe: Optional[str]
    faixa_etaria: Optional[str]
    qtd_atendimentos_12m: int
    data_ultimo_atendimento: Optional[date]

    class Config:
        orm_mode = True

    @validator("hash_identificador", pre=False, always=False)
    def mask_hash(cls, v):
        return mask_hash_identificador(v) if v else v


class CriancaOut(BaseModel):
    id_paciente: int
    hash_identificador: Optional[str]
    municipio: str
    codigo_ibge: str
    unidade: Optional[str]
    codigo_unidade: Optional[str]
    equipe: Optional[str]
    codigo_equipe: Optional[str]
    faixa_etaria: Optional[str]
    qtd_atendimentos_12m: int
    data_ultimo_atendimento: Optional[date]

    class Config:
        orm_mode = True

    @validator("hash_identificador", pre=False, always=False)
    def mask_hash(cls, v):
        return mask_hash_identificador(v) if v else v
