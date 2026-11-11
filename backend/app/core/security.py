"""JWT 签发与登录态校验。"""

import os
from datetime import UTC, datetime, timedelta

from fastapi import Header, HTTPException, status
from jose import JWTError, jwt

APP_ENV = os.getenv("APP_ENV", "dev").strip().lower()
MIN_SECRET_LENGTH = 32
DEV_FALLBACK_SECRET = "dev-only-insecure-secret"


def _load_secret_key() -> str:
    """读取签名密钥：非 dev 环境缺失或过短时直接终止启动，避免 token 被伪造。"""
    secret = (os.getenv("AUTH_SECRET") or "").strip()
    if not secret:
        if APP_ENV == "dev":
            return DEV_FALLBACK_SECRET
        raise RuntimeError("AUTH_SECRET 未配置：非 dev 环境必须通过环境变量提供签名密钥")
    if len(secret) < MIN_SECRET_LENGTH:
        raise RuntimeError(f"AUTH_SECRET 至少需要 {MIN_SECRET_LENGTH} 位，当前 {len(secret)} 位")
    return secret


SECRET_KEY = _load_secret_key()
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "120"))


def create_access_token(subject: str) -> str:
    """签发 JWT：sub 存放用户唯一标识（openid）。"""
    expire = datetime.now(UTC) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    payload = {"sub": subject, "exp": expire}
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)


def verify_access_token(token: str) -> str | None:
    """校验 JWT，成功返回 openid，失败（伪造/过期/缺 sub）返回 None。"""
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    except JWTError:
        return None
    openid = payload.get("sub")
    if not openid:
        return None
    return str(openid)


async def get_current_user_openid(authorization: str | None = Header(default=None)) -> str:
    """登录态依赖：从 Authorization: Bearer <token> 取 token 并校验。

    未携带、格式不对、校验失败统一返回 401，路由侧无需重复判断。
    """
    if not authorization or not authorization.strip():
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="未携带 token，请先登录",
            headers={"WWW-Authenticate": "Bearer"},
        )

    parts = authorization.split()
    if len(parts) != 2 or parts[0].lower() != "bearer":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authorization 头格式应为 Bearer <token>",
            headers={"WWW-Authenticate": "Bearer"},
        )

    openid = verify_access_token(parts[1])
    if openid is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="token 无效或已过期，请重新登录",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return openid
