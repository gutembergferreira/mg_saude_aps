from datetime import date

from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from ..db.base import Base
from ..db.session import get_db
from ..main import app
from ..models.dw import DimIndicador, DimMunicipio, DimTempo, FatoIndicadorAPS


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
        municipio = DimMunicipio(
            id_municipio=1,
            codigo_ibge="2611606",
            nome="Recife",
            uf="PE",
        )
        indicador_c1 = DimIndicador(id_indicador=1, codigo="C1", nome="Indicador C1")
        indicador_c2 = DimIndicador(id_indicador=2, codigo="C2", nome="Indicador C2")

        tempo_q1 = DimTempo(
            id_tempo=1,
            data=date(2025, 1, 1),
            ano=2025,
            mes=1,
            dia=1,
            trimestre=1,
            quadrimestre=1,
            nome_mes="January",
            nome_dia_semana="Wednesday",
            eh_final_semana=False,
        )
        tempo_q2 = DimTempo(
            id_tempo=2,
            data=date(2025, 4, 1),
            ano=2025,
            mes=4,
            dia=1,
            trimestre=2,
            quadrimestre=2,
            nome_mes="April",
            nome_dia_semana="Tuesday",
            eh_final_semana=False,
        )

        fato1 = FatoIndicadorAPS(
            id_fato_ind=1,
            id_tempo=1,
            id_municipio=1,
            id_indicador=1,
            periodo_referencia="2025Q1",
            valor=0.85,
            meta=0.8,
            atingiu_meta=True,
        )
        fato2 = FatoIndicadorAPS(
            id_fato_ind=2,
            id_tempo=2,
            id_municipio=1,
            id_indicador=1,
            periodo_referencia="2025Q2",
            valor=0.5,
            meta=0.8,
            atingiu_meta=False,
        )
        fato3 = FatoIndicadorAPS(
            id_fato_ind=3,
            id_tempo=1,
            id_municipio=1,
            id_indicador=2,
            periodo_referencia="2025Q1",
            valor=0.9,
            meta=0.85,
            atingiu_meta=True,
        )

        session.add_all([municipio, indicador_c1, indicador_c2, tempo_q1, tempo_q2, fato1, fato2, fato3])
        session.commit()
    finally:
        session.close()


app.dependency_overrides[get_db] = override_get_db
_setup_database()
client = TestClient(app)


def test_listar_indicadores_retorna_todos():
    response = client.get("/api/v1/indicadores/2611606")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 3
    codigos = sorted([item["indicador"] for item in data])
    assert codigos == ["C1", "C1", "C2"]


def test_filtra_por_indicador():
    response = client.get("/api/v1/indicadores/2611606?indicador=C1")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2
    assert all(item["indicador"] == "C1" for item in data)


def test_filtra_por_periodo():
    response = client.get("/api/v1/indicadores/2611606?periodo=2025Q1")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2
    periodos = {item["periodo_referencia"] for item in data}
    assert periodos == {"2025Q1"}
