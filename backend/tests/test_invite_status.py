"""
测试邀约人数满员自动切换状态
"""
# noqa: I001
from pathlib import Path
import sys
from fastapi.testclient import TestClient

sys.path.insert(0, str(Path(__file__).parent.parent))
from main import app

client = TestClient(app)

def test_join_invite_auto_full():
    """测试：加入后人数达到上限，自动变为已满状态"""
    resp1 = client.post("/invite/join", json={"invite_id": 1, "user_id": 2})
    assert resp1.status_code == 200
    data1 = resp1.json()
    assert data1["invite"]["current_count"] == 2
    assert data1["invite"]["status"] == "recruiting"

    resp2 = client.post("/invite/join", json={"invite_id": 1, "user_id": 3})
    assert resp2.status_code == 200
    data2 = resp2.json()
    assert data2["invite"]["current_count"] == 3
    assert data2["invite"]["status"] == "full"

    resp3 = client.post("/invite/join", json={"invite_id": 1, "user_id": 4})
    assert resp3.status_code == 400
    assert "名额已满" in resp3.json()["detail"]
