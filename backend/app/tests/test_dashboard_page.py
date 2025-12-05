from fastapi.testclient import TestClient

from ..main import app

client = TestClient(app)


def test_dashboard_page_renders():
    resp = client.get("/dashboard")
    assert resp.status_code == 200
    assert "Dashboard APS – Visão Geral" in resp.text
