from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_param_exception():
    # 模拟一个会触发参数校验失败的接口，这里示例，你可以替换成真实接口
    resp = client.get("/api/test-demo")
    assert resp.json()["code"] in (40001, 400)
