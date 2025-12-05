from pydantic import BaseModel
from typing import Optional


class IndicadorAPSOut(BaseModel):
    municipio: str
    codigo_ibge: str
    indicador: str
    nome_indicador: str
    periodo_referencia: str
    valor: Optional[float]
    meta: Optional[float]
    atingiu_meta: Optional[bool]

    class Config:
        orm_mode = True
