"""邀约发布接口（issue #5）单元测试。"""

from datetime import UTC, datetime, timedelta

import pytest
from fastapi.testclient import TestClient

from app.main import app
from app.repositories import invitation_repo

client = TestClient(app)

HEADERS = {"X-User-Id": "9001"}


def future_time(days: int = 1) -> str:
    return (datetime.now(UTC) + timedelta(days=days)).isoformat()


def make_payload(**overrides):
    payload = {
        "title": "周末羽毛球搭子",
        "type": "sport",
        "location": "东区体育馆",
        "start_time": future_time(),
        "max_count": 4,
        "description": "水平不限，主要想活动一下。",
    }
    payload.update(overrides)
    return payload


def error_fields(response) -> set[tuple[str, ...]]:
    return {tuple(item["loc"]) for item in response.json()["detail"]}


@pytest.fixture(autouse=True)
def clean_store():
    invitation_repo.reset_store()
    yield
    invitation_repo.reset_store()


def test_publish_requires_login():
    response = client.post("/api/invitations", json=make_payload())
    assert response.status_code == 401
    assert "未登录" in response.json()["detail"]


def test_publish_success_returns_server_controlled_fields():
    response = client.post("/api/invitations", json=make_payload(), headers=HEADERS)

    assert response.status_code == 201
    data = response.json()
    assert data["status"] == "recruiting"
    assert data["current_count"] == 1
    assert data["publisher_id"] == 9001
    assert data["title"] == "周末羽毛球搭子"
    assert data["max_count"] == 4

    detail = client.get(f"/api/invitations/{data['id']}")
    assert detail.status_code == 200
    assert detail.json()["id"] == data["id"]


def test_published_invitation_appears_first_in_square():
    created = client.post("/api/invitations", json=make_payload(), headers=HEADERS).json()

    response = client.get("/api/invitations", params={"type": "sport"})
    assert response.status_code == 200
    assert response.json()["list"][0]["id"] == created["id"]


def test_forged_status_field_is_ignored():
    response = client.post(
        "/api/invitations",
        json=make_payload(status="full", current_count=99),
        headers=HEADERS,
    )
    assert response.status_code == 201
    assert response.json()["status"] == "recruiting"
    assert response.json()["current_count"] == 1


def test_title_too_short_rejected():
    response = client.post("/api/invitations", json=make_payload(title="abc"), headers=HEADERS)
    assert response.status_code == 422
    assert ("body", "title") in error_fields(response)


def test_title_is_trimmed_before_length_check():
    response = client.post(
        "/api/invitations", json=make_payload(title="   ab   "), headers=HEADERS
    )
    assert response.status_code == 422
    assert ("body", "title") in error_fields(response)


def test_title_too_long_rejected():
    response = client.post(
        "/api/invitations", json=make_payload(title="搭" * 31), headers=HEADERS
    )
    assert response.status_code == 422


def test_start_time_in_past_rejected():
    response = client.post(
        "/api/invitations",
        json=make_payload(start_time=(datetime.now(UTC) - timedelta(hours=1)).isoformat()),
        headers=HEADERS,
    )
    assert response.status_code == 422
    assert ("body", "start_time") in error_fields(response)


def test_start_time_without_timezone_rejected():
    response = client.post(
        "/api/invitations",
        json=make_payload(start_time="2099-01-01T19:00:00"),
        headers=HEADERS,
    )
    assert response.status_code == 422
    assert ("body", "start_time") in error_fields(response)


def test_start_time_too_far_ahead_rejected():
    response = client.post(
        "/api/invitations", json=make_payload(start_time=future_time(days=31)), headers=HEADERS
    )
    assert response.status_code == 422
    assert ("body", "start_time") in error_fields(response)


@pytest.mark.parametrize("max_count", [1, 21])
def test_max_count_out_of_range_rejected(max_count):
    response = client.post(
        "/api/invitations", json=make_payload(max_count=max_count), headers=HEADERS
    )
    assert response.status_code == 422
    assert ("body", "max_count") in error_fields(response)


def test_invalid_type_rejected():
    response = client.post(
        "/api/invitations", json=make_payload(type="singing"), headers=HEADERS
    )
    assert response.status_code == 422
    assert ("body", "type") in error_fields(response)


def test_description_too_long_rejected():
    response = client.post(
        "/api/invitations", json=make_payload(description="搭" * 501), headers=HEADERS
    )
    assert response.status_code == 422
    assert ("body", "description") in error_fields(response)
