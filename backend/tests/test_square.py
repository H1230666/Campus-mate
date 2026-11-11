"""邀约广场模块单元测试。"""

from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_list_default_pagination():
    resp = client.get("/api/invitations")
    assert resp.status_code == 200
    data = resp.json()
    assert data["page"] == 1
    assert data["page_size"] == 10
    assert data["total"] >= 1
    assert len(data["list"]) <= 10
    assert data["list"] == sorted(data["list"], key=lambda x: x["created_at"], reverse=True)


def test_list_page_size_upper_bound_is_rejected():
    resp = client.get("/api/invitations", params={"page_size": 999})
    assert 400 <= resp.status_code < 500


def test_filter_by_type():
    resp = client.get("/api/invitations", params={"type": "study"})
    assert resp.status_code == 200
    assert all(item["type"] == "study" for item in resp.json()["list"])


def test_filter_invalid_type_is_client_error():
    resp = client.get("/api/invitations", params={"type": "unknown"})
    assert 400 <= resp.status_code < 500


def test_page_out_of_range_returns_empty_list():
    resp = client.get("/api/invitations", params={"page": 1000})
    assert resp.status_code == 200
    assert resp.json()["list"] == []


def test_get_invitation_detail():
    resp = client.get("/api/invitations/1")
    assert resp.status_code == 200
    assert resp.json()["id"] == 1


def test_get_invitation_not_found():
    resp = client.get("/api/invitations/99999")
    assert resp.status_code == 404


def test_filter_by_status():
    resp = client.get("/api/invitations", params={"status": "full"})
    assert resp.status_code == 200
    assert all(item["status"] == "full" for item in resp.json()["list"])


def test_filter_invalid_status_is_client_error():
    resp = client.get("/api/invitations", params={"status": "unknown"})
    assert 400 <= resp.status_code < 500
