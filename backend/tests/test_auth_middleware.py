"""登录态鉴权测试：正常、缺失、格式错误、伪造、过期五类场景。

对应 Issue #2 验收标准：token 登录态校验中间件，未登录接口拦截。
"""

import asyncio
from datetime import UTC, datetime, timedelta

import pytest
from fastapi import HTTPException
from jose import jwt

from app.core.auth import (
    ALGORITHM,
    SECRET_KEY,
    create_access_token,
    get_current_user_openid,
    verify_access_token,
)


def test_token_roundtrip_returns_openid():
    token = create_access_token("o123456789abcdef")
    assert verify_access_token(token) == "o123456789abcdef"


def test_token_signed_by_other_secret_is_rejected():
    fake = jwt.encode({"sub": "attacker"}, "another-secret", algorithm=ALGORITHM)
    assert verify_access_token(fake) is None


def test_malformed_token_is_rejected():
    assert verify_access_token("not-a-jwt") is None


def test_expired_token_is_rejected():
    expired = jwt.encode(
        {"sub": "o123", "exp": datetime.now(UTC) - timedelta(minutes=1)},
        SECRET_KEY,
        algorithm=ALGORITHM,
    )
    assert verify_access_token(expired) is None


def test_missing_authorization_header_raises_401():
    with pytest.raises(HTTPException) as err:
        asyncio.run(get_current_user_openid(None))
    assert err.value.status_code == 401


def test_wrong_scheme_raises_401():
    with pytest.raises(HTTPException) as err:
        asyncio.run(get_current_user_openid("Token abc.def.ghi"))
    assert err.value.status_code == 401


def test_bearer_with_invalid_token_raises_401():
    with pytest.raises(HTTPException) as err:
        asyncio.run(get_current_user_openid("Bearer not-a-jwt"))
    assert err.value.status_code == 401


def test_bearer_with_valid_token_returns_openid():
    token = create_access_token("o123456789abcdef")
    assert asyncio.run(get_current_user_openid(f"Bearer {token}")) == "o123456789abcdef"
