from fastapi.testclient import TestClient

from src.main import app

client = TestClient(app)


def test_viewer_cannot_create_datasource():
    resp = client.post(
        "/api/v1/datasources",
        json={"name": "ds1", "type": "mysql"},
    )
    assert resp.status_code == 403


def test_admin_can_create_datasource():
    resp = client.post(
        "/api/v1/datasources",
        headers={"x-role": "admin"},
        json={"name": "ds_admin", "type": "postgresql"},
    )
    assert resp.status_code == 200
    assert resp.json()["name"] == "ds_admin"


def test_unknown_role_rejected():
    resp = client.post(
        "/api/v1/datasources",
        headers={"x-role": "ghost"},
        json={"name": "ds_ghost", "type": "postgresql"},
    )
    assert resp.status_code == 401
