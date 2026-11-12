"""全局异常处理器统一错误响应测试。"""

from fastapi.testclient import TestClient

from app.core.exceptions import BusinessException, ErrorCode
from app.main import app


@app.get("/_test/business-error")
def _raise_business_error() -> None:
    raise BusinessException(ErrorCode.BAD_REQUEST, "业务失败提示")


@app.get("/_test/unhandled-error")
def _raise_unhandled_error() -> None:
    raise RuntimeError("boom-secret")


client = TestClient(app, raise_server_exceptions=False)


def test_business_exception_returns_unified_body():
    resp = client.get("/_test/business-error")
    assert resp.status_code == 400
    body = resp.json()
    assert body["code"] == ErrorCode.BAD_REQUEST.value
    assert body["msg"] == "业务失败提示"
    assert body["data"] is None


def test_http_exception_returns_unified_body():
    resp = client.get("/api/invitations/99999")
    assert resp.status_code == 404
    body = resp.json()
    assert body["code"] == 404
    assert body["msg"] == "invitation not found"
    assert body["data"] is None


def test_validation_error_returns_unified_body():
    resp = client.post("/api/invitations", json={}, headers={"X-User-Id": "9001"})
    assert resp.status_code == 422
    body = resp.json()
    assert body["code"] == ErrorCode.PARAM_VALIDATE_ERROR.value
    assert body["msg"] == "参数校验失败"
    assert isinstance(body["data"], list)
    assert body["data"]


def test_unhandled_exception_returns_500_without_leak():
    resp = client.get("/_test/unhandled-error")
    assert resp.status_code == 500
    body = resp.json()
    assert body["code"] == ErrorCode.INTERNAL_ERROR.value
    assert body["msg"] == "服务器内部异常"
    assert "boom-secret" not in resp.text
