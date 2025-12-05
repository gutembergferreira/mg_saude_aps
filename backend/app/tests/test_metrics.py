from fastapi.testclient import TestClient

from ..main import app


client = TestClient(app)


def test_metrics_endpoint():
    resp = client.get("/metrics")
    assert resp.status_code == 200
    body = resp.text
    assert "mg_saude_requests_total" in body
