from fastapi.testclient import TestClient

from ..main import app

client = TestClient(app)


def test_get_login_page():
    resp = client.get("/login")
    assert resp.status_code == 200
    assert "Entrar" in resp.text


def test_root_redirects_to_login():
    resp = client.get("/", allow_redirects=False)
    assert resp.status_code in (302, 307)
    assert resp.headers["location"].endswith("/login")
