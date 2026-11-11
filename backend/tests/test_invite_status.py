import sys
from pathlib import Path
# 把backend根目录加入搜索路径
sys.path.insert(0, str(Path(__file__).parent.parent))

from fastapi.testclient import TestClient  # noqa: I001
from main import app

client = TestClient(app)


def test_join_invite_auto_full():
    """测试：加入后人数达到上限，自动变为已满状态"""
    # 初始邀约id=1，max=3，current=1
    # 第一次加入
    resp1 = client.post("/invite/join", json={"invite_id":1, "user_id":2})
    assert resp1.status_code == 200
    data1 = resp1.json()
    assert data1["invite"]["current_count"] == 2
    assert data1["invite"]["status"] == "recruiting"

    # 第二次加入，刚好满3人，自动变成full
    resp2 = client.post("/invite/join", json={"invite_id":1, "user_id":3})
    assert resp2.status_code == 200
    data2 = resp2.json()
    assert data2["invite"]["current_count"] == 3
    assert data2["invite"]["status"] == "full"

    # 第三次加入，已满，拒绝
    resp3 = client.post("/invite/join", json={"invite_id":1, "user_id":4})
    assert resp3.status_code == 400
    assert "名额已满" in resp3.json()["detail"]
