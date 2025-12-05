from datetime import date
from typing import Optional

from pydantic import BaseModel


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
