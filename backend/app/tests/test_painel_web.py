from fastapi.testclient import TestClient

from ..main import app

client = TestClient(app)


def test_painel_gestantes_page():
    resp = client.get("/painel/gestantes")
    assert resp.status_code == 200
    assert "Painel de Gestantes" in resp.text


def test_painel_criancas_page():
    resp = client.get("/painel/criancas")
    assert resp.status_code == 200
    assert "Painel de Crianças" in resp.text
