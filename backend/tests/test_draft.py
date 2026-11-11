"""草稿暂存接口（issue #6）单元测试。"""

import pytest
from fastapi.testclient import TestClient

from app.main import app
from app.repositories import invitation_repo

client = TestClient(app)

USER_B = {"X-User-Id": "9002"}
USER_C = {"X-User-Id": "9003"}


@pytest.fixture(autouse=True)
def clean_store():
    invitation_repo.reset_store()
    yield
    invitation_repo.reset_store()


def test_get_draft_returns_null_when_absent():
    response = client.get("/api/invitations/draft", headers=USER_B)
    assert response.status_code == 200
    assert response.json() is None


def test_save_draft_with_partial_fields():
    response = client.put(
        "/api/invitations/draft",
        json={"title": "周五晚上剧本杀"},
        headers=USER_B,
    )
    assert response.status_code == 200
    draft = response.json()
    assert draft["title"] == "周五晚上剧本杀"
    assert draft["updated_at"]

    fetched = client.get("/api/invitations/draft", headers=USER_B).json()
    assert fetched["title"] == "周五晚上剧本杀"


def test_save_draft_merges_previous_fields():
    client.put("/api/invitations/draft", json={"title": "周五剧本杀"}, headers=USER_B)
    client.put("/api/invitations/draft", json={"location": "北门剧本杀店"}, headers=USER_B)

    draft = client.get("/api/invitations/draft", headers=USER_B).json()
    assert draft["title"] == "周五剧本杀"
    assert draft["location"] == "北门剧本杀店"


def test_save_draft_can_clear_a_field():
    client.put("/api/invitations/draft", json={"title": "周五剧本杀"}, headers=USER_B)
    response = client.put("/api/invitations/draft", json={"title": ""}, headers=USER_B)

    assert response.status_code == 200
    assert response.json()["title"] == ""


def test_drafts_are_isolated_between_users():
    client.put("/api/invitations/draft", json={"title": "B 的草稿"}, headers=USER_B)

    response = client.get("/api/invitations/draft", headers=USER_C)
    assert response.json() is None


def test_delete_draft_is_idempotent():
    client.put("/api/invitations/draft", json={"title": "待删除草稿"}, headers=USER_B)

    first = client.delete("/api/invitations/draft", headers=USER_B)
    assert first.status_code == 204
    assert client.get("/api/invitations/draft", headers=USER_B).json() is None

    second = client.delete("/api/invitations/draft", headers=USER_B)
    assert second.status_code == 204


def test_draft_is_not_visible_in_square():
    title = "只存在草稿箱里的邀约"
    client.put("/api/invitations/draft", json={"title": title}, headers=USER_B)

    response = client.get("/api/invitations", params={"page_size": 50})
    titles = [item["title"] for item in response.json()["list"]]
    assert title not in titles


def test_invalid_draft_field_rejected():
    response = client.put(
        "/api/invitations/draft",
        json={"max_count": 1},
        headers=USER_B,
    )
    assert response.status_code == 422
    assert ("body", "max_count") in {tuple(item["loc"]) for item in response.json()["detail"]}


def test_draft_requires_login():
    response = client.put("/api/invitations/draft", json={"title": "匿名草稿"})
    assert response.status_code == 401
