"""邀约报名：满员自动切换状态、人数上限控制。"""

from datetime import UTC, datetime, timedelta

import pytest
from fastapi.testclient import TestClient

from app.main import app
from app.repositories import invitation_repo

client = TestClient(app)


@pytest.fixture(autouse=True)
def clean_store():
    invitation_repo.reset_store()
    yield
    invitation_repo.reset_store()


def _publish(max_count: int) -> int:
    """发布一条指定人数上限的邀约，返回其 id。"""
    resp = client.post(
        "/api/invitations",
        json={
            "title": "图书馆自习搭子",
            "type": "study",
            "location": "图书馆三楼自习区",
            "start_time": (datetime.now(UTC) + timedelta(days=1)).isoformat(),
            "max_count": max_count,
        },
        headers={"X-User-Id": "9001"},
    )
    assert resp.status_code == 201
    return resp.json()["id"]


def test_join_auto_full_and_reject_extra():
    invitation_id = _publish(max_count=3)

    # 第 2 人加入：未达上限，仍为招募中
    resp1 = client.post(
        f"/api/invitations/{invitation_id}/join", headers={"X-User-Id": "9002"}
    )
    assert resp1.status_code == 200
    data1 = resp1.json()
    assert data1["current_count"] == 2
    assert data1["status"] == "recruiting"

    # 第 3 人加入：达到上限，自动置为已满
    resp2 = client.post(
        f"/api/invitations/{invitation_id}/join", headers={"X-User-Id": "9003"}
    )
    assert resp2.status_code == 200
    data2 = resp2.json()
    assert data2["current_count"] == 3
    assert data2["status"] == "full"

    # 第 4 人再加入：拒绝并提示名额已满
    resp3 = client.post(
        f"/api/invitations/{invitation_id}/join", headers={"X-User-Id": "9004"}
    )
    assert resp3.status_code == 400
    assert "名额已满" in resp3.json()["msg"]
