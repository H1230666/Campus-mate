"""JWT 签发与登录态校验。"""

import os
from datetime import UTC, datetime, timedelta

from fastapi import Header, HTTPException, status
from jose import JWTError, jwt

# 密钥从环境变量读取，仓库里不留真实密钥；本地未配置时用开发默认值。
SECRET_KEY = os.getenv("SECRET_KEY", "dev-only-insecure-secret")
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
