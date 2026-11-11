"""用户认证与个人信息接口。"""

import os

from fastapi import APIRouter, Depends, HTTPException, status

from app.core.auth import create_access_token, get_current_user_openid
from app.schemas.user_auth_schema import UserInfoUpdateRequest, WxLoginRequest

router = APIRouter(prefix="/api/user", tags=["用户认证模块"])

# 微信登录目前把前端 code 直接当 openid（mock），仅 dev 环境开放，
# 避免任意字符串都能换到合法登录态。
MOCK_WX_LOGIN = os.getenv("APP_ENV", "dev").strip().lower() == "dev"


@router.post("/wx-login", summary="微信小程序授权登录")
async def wx_login(req: WxLoginRequest) -> dict:
    if not MOCK_WX_LOGIN:
        raise HTTPException(
            status_code=status.HTTP_501_NOT_IMPLEMENTED,
            detail="微信登录尚未接入 jscode2session，暂不可用",
        )
    # TODO(#2): 用 code 调微信 jscode2session 换取真实 openid 后再签发 token。
    openid = req.code
    return {
        "code": 200,
        "msg": "登录成功",
        "data": {"token": create_access_token(subject=openid), "openid": openid},
    }


@router.get("/info", summary="获取个人信息（需登录）")
async def get_user_info(openid: str = Depends(get_current_user_openid)) -> dict:
    return {
        "code": 200,
        "msg": "查询成功",
        "data": {
            "openid": openid,
            "nickname": "校园搭子用户",
            "avatar": "",
            "interest_tags": [],
            "create_time": "2026-11-05",
        },
    }


@router.put("/info", summary="修改个人信息（需登录）")
async def update_user_info(
    update_data: UserInfoUpdateRequest,
    openid: str = Depends(get_current_user_openid),
) -> dict:
    return {
        "code": 200,
        "msg": "用户信息修改成功",
        "data": {"openid": openid, "update": update_data.model_dump(exclude_unset=True)},
    }
