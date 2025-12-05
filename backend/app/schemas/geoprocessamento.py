from typing import Optional
from pydantic import BaseModel


class UnidadeGeoOut(BaseModel):
    id_unidade: int
    codigo_cnes: str
    nome: str
    latitude: Optional[float]
    longitude: Optional[float]
    quantidade_cadastros: int
    quantidade_atendimentos_12m: int

    class Config:
        orm_mode = True


class IndicadorUnidadeGeoOut(BaseModel):
    id_unidade: int
    codigo_cnes: str
    nome: str
    latitude: Optional[float]
    longitude: Optional[float]
    valor_indicador: Optional[float]
    meta: Optional[float]
    atingiu_meta: Optional[bool]

    class Config:
        orm_mode = True


class IndicadorTerritorioGeoOut(BaseModel):
    id_territorio: int
    codigo_territorio: str
    descricao: Optional[str]
    latitude: Optional[float]
    longitude: Optional[float]
    valor_indicador: Optional[float]
    meta: Optional[float]
    atingiu_meta: Optional[bool]

    class Config:
        orm_mode = True
