from datetime import date, timedelta

from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from ..db.base import Base
from ..db.session import get_db
from ..main import app
from ..models.dw import (
    DimEquipe,
    DimMunicipio,
    DimPaciente,
    DimTempo,
    DimUnidadeSaude,
    FatoAtendimentoAPS,
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
        unidade = DimUnidadeSaude(id_unidade=1, codigo_cnes="1234567", nome="USF X", id_municipio=1)
        equipe = DimEquipe(id_equipe=1, codigo_equipe="E001", descricao="ESF 001", id_unidade=1)

        # Datas de atendimento (dentro dos últimos 12 meses)
        hoje = date.today()
        recente = hoje - timedelta(days=30)
        recente2 = hoje - timedelta(days=60)

        tempo1 = DimTempo(
            id_tempo=1,
            data=recente,
            ano=recente.year,
            mes=recente.month,
            dia=recente.day,
            trimestre=(recente.month - 1) // 3 + 1,
            quadrimestre=(recente.month - 1) // 4 + 1,
            nome_mes="Mes",
            nome_dia_semana="Dia",
            eh_final_semana=False,
        )
        tempo2 = DimTempo(
            id_tempo=2,
            data=recente2,
            ano=recente2.year,
            mes=recente2.month,
            dia=recente2.day,
            trimestre=(recente2.month - 1) // 3 + 1,
            quadrimestre=(recente2.month - 1) // 4 + 1,
            nome_mes="Mes",
            nome_dia_semana="Dia",
            eh_final_semana=False,
        )

        gestante = DimPaciente(
            id_paciente=1,
            id_municipio=1,
            sexo="F",
            faixa_etaria="20-24",
            hash_identificador="hash_gest",
        )
        outra_mulher = DimPaciente(
            id_paciente=2,
            id_municipio=1,
            sexo="F",
            faixa_etaria="25-29",
            hash_identificador="hash_outro",
        )
        crianca = DimPaciente(
            id_paciente=3,
            id_municipio=1,
            sexo="M",
            faixa_etaria="0-1",
            hash_identificador="hash_crianca",
        )

        atendimento_gestante = FatoAtendimentoAPS(
            id_fato_atend=1,
            id_tempo=1,
            id_municipio=1,
            id_unidade=1,
            id_equipe=1,
            id_paciente=1,
            tipo_atendimento="Consulta gestante",
            codigo_proced="PRENATAL_1",
            quantidade=1,
        )
        atendimento_outro = FatoAtendimentoAPS(
            id_fato_atend=2,
            id_tempo=2,
            id_municipio=1,
            id_unidade=1,
            id_equipe=1,
            id_paciente=2,
            tipo_atendimento="Consulta geral",
            codigo_proced="CONSULTA",
            quantidade=1,
        )
        atendimento_crianca = FatoAtendimentoAPS(
            id_fato_atend=3,
            id_tempo=1,
            id_municipio=1,
            id_unidade=1,
            id_equipe=1,
            id_paciente=3,
            tipo_atendimento="Consulta puericultura",
            codigo_proced="CONSULTA",
            quantidade=1,
        )

        session.add_all(
            [
                municipio,
                unidade,
                equipe,
                tempo1,
                tempo2,
                gestante,
                outra_mulher,
                crianca,
                atendimento_gestante,
                atendimento_outro,
                atendimento_crianca,
            ]
        )
        session.commit()
    finally:
        session.close()


app.dependency_overrides[get_db] = override_get_db
_setup_database()
client = TestClient(app)


def test_painel_gestantes_retorna_apenas_gestantes():
    resp = client.get("/api/v1/painel/gestantes/2611606")
    assert resp.status_code == 200
    data = resp.json()
    assert len(data) == 1
    item = data[0]
    assert item["id_paciente"] == 1
    assert item["codigo_unidade"] == "1234567"
    assert item["codigo_equipe"] == "E001"
    assert item["qtd_atendimentos_12m"] == 1


def test_painel_criancas_filtra_faixa_etaria():
    resp = client.get("/api/v1/painel/criancas/2611606?faixa_etaria=0-1")
    assert resp.status_code == 200
    data = resp.json()
    assert len(data) == 1
    assert data[0]["id_paciente"] == 3
    assert data[0]["faixa_etaria"] == "0-1"
