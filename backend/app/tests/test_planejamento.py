from datetime import datetime

from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from ..db.base import Base
from ..db.session import get_db
from ..main import app
from ..models.dw import DimMunicipio


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
        session.add(municipio)
        session.commit()
    finally:
        session.close()


app.dependency_overrides[get_db] = override_get_db
_setup_database()
client = TestClient(app)


def test_criar_problema_gut_calcula_score():
    payload = {
        "id_municipio": 1,
        "titulo": "Falta de insumos",
        "gravidade": 5,
        "urgencia": 4,
        "tendencia": 3,
        "descricao": "Risco de desabastecimento",
    }
    resp = client.post("/api/v1/planejamento/problemas", json=payload)
    assert resp.status_code == 201
    data = resp.json()
    assert data["score_gut"] == 5 * 4 * 3
    assert data["status"] == "planejado"


def test_listar_problemas_por_municipio():
    resp = client.get("/api/v1/planejamento/problemas?codigo_ibge=2611606")
    assert resp.status_code == 200
    data = resp.json()
    assert isinstance(data, list)
    assert len(data) >= 1


def test_criar_e_listar_acoes():
    # cria um problema para vincular ação
    resp_prob = client.post(
        "/api/v1/planejamento/problemas",
        json={
            "id_municipio": 1,
            "titulo": "Capacitar equipe",
            "gravidade": 3,
            "urgencia": 3,
            "tendencia": 3,
        },
    )
    assert resp_prob.status_code == 201
    problema_id = resp_prob.json()["id"]

    acao_payload = {
        "problema_id": problema_id,
        "descricao": "Realizar treinamento",
        "responsavel": "Coordenador",
    }
    resp_acao = client.post("/api/v1/planejamento/acoes", json=acao_payload)
    assert resp_acao.status_code == 201

    resp_list = client.get(f"/api/v1/planejamento/acoes/{problema_id}")
    assert resp_list.status_code == 200
    data = resp_list.json()
    assert len(data) == 1
    assert data[0]["descricao"] == "Realizar treinamento"
