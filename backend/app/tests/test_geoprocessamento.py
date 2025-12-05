from datetime import date

from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from ..db.base import Base
from ..db.session import get_db
from ..main import app
from ..models.dw import (
    DimIndicador,
    DimMunicipio,
    DimTerritorio,
    DimTempo,
    DimUnidadeSaude,
    FatoAtendimentoAPS,
    FatoCadastroAPS,
    FatoIndicadorAPS,
)

engine = create_engine(
    "sqlite:///:memory:",
    connect_args={"check_same_thread": False},
)
SessionTesting = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine.execution_options(schema_translate_map={"dw": None}),
)


def override_get_db():
    db = SessionTesting()
    try:
        yield db
    finally:
        db.close()


def _setup_database():
    with engine.begin() as conn:
        conn = conn.execution_options(schema_translate_map={"dw": None})
        Base.metadata.create_all(bind=conn)

    session = SessionTesting()
    try:
        municipio = DimMunicipio(id_municipio=1, codigo_ibge="2611606", nome="Recife", uf="PE")
        tempo = DimTempo(
            id_tempo=1,
            data=date.today(),
            ano=date.today().year,
            mes=date.today().month,
            dia=date.today().day,
            trimestre=(date.today().month - 1) // 3 + 1,
            quadrimestre=(date.today().month - 1) // 4 + 1,
            nome_mes="Mes",
            nome_dia_semana="Dia",
            eh_final_semana=False,
        )
        unidade = DimUnidadeSaude(
            id_unidade=1,
            codigo_cnes="1234567",
            nome="USF X",
            id_municipio=1,
            latitude=-8.055,
            longitude=-34.951,
        )
        territorio = DimTerritorio(
            id_territorio=1,
            codigo_territorio="T001",
            descricao="Território 1",
            latitude=-8.056,
            longitude=-34.952,
            id_equipe=None,
        )
        indicador = DimIndicador(id_indicador=1, codigo="C1", nome="Indicador C1")

        fato_cad = FatoCadastroAPS(
            id_fato_cad=1,
            id_tempo=1,
            id_municipio=1,
            id_unidade=1,
            cadastro_valido=True,
            eh_publico_alvo=True,
            peso_capitacao=1,
        )
        fato_at = FatoAtendimentoAPS(
            id_fato_atend=1,
            id_tempo=1,
            id_municipio=1,
            id_unidade=1,
            quantidade=1,
        )
        fato_ind = FatoIndicadorAPS(
            id_fato_ind=1,
            id_tempo=1,
            id_municipio=1,
            id_unidade=1,
            id_territorio=1,
            id_indicador=1,
            periodo_referencia="2025Q1",
            valor=0.82,
            meta=0.8,
            atingiu_meta=True,
        )

        session.add_all([municipio, tempo, unidade, territorio, indicador, fato_cad, fato_at, fato_ind])
        session.commit()
    finally:
        session.close()


app.dependency_overrides[get_db] = override_get_db
_setup_database()
client = TestClient(app)


def test_geo_unidades_retorna_dados():
    resp = client.get("/api/v1/geo/unidades/2611606")
    assert resp.status_code == 200
    data = resp.json()
    assert len(data) == 1
    assert data[0]["codigo_cnes"] == "1234567"
    assert data[0]["quantidade_cadastros"] == 1


def test_geo_indicador_por_unidade():
    resp = client.get("/api/v1/geo/indicador/2611606?indicador=C1&periodo=2025Q1&nivel=unidade")
    assert resp.status_code == 200
    data = resp.json()
    assert len(data) == 1
    assert data[0]["valor_indicador"] == 0.82
    assert data[0]["atingiu_meta"] is True
