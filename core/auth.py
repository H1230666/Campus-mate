from datetime import datetime, timedelta
from typing import Optional
from jose import JWTError, jwt
from fastapi import Depends, HTTPException, status

SECRET_KEY = "campus-mate-secret-2026-jnu-project"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 120

def create_access_token(subject: str):
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode = {"sub": subject, "exp": expire}
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def verify_access_token(token: str) -> Optional[str]:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        openid: str = payload.get("sub")
        if openid is None:
            return None
        return openid
    except JWTError:
        return None

async def get_current_user_openid(token: Optional[str] = None):
    if token is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="未携带token，请先登录",
            headers={"WWW-Authenticate": "Bearer"},
        )
    openid = verify_access_token(token)
    if openid is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="token无效或已过期，请重新登录",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return openid
