from fastapi import APIRouter, Depends, HTTPException
from backend.app.schemas.user_auth_schema import WxLoginRequest, UserInfoUpdateRequest
from backend.app.core.auth import create_access_token, get_current_user_openid


router = APIRouter(prefix="/api/user", tags=["用户认证模块"])

@router.post("/wx-login", summary="微信小程序授权登录")
async def wx_login(req: WxLoginRequest):
    openid = req.code
    token = create_access_token(subject=openid)
    return {
        "code": 200,
        "msg": "登录成功",
        "data": {
            "token": token,
            "openid": openid
        }
    }

@router.get("/info", summary="获取个人信息，需要登录态")
async def get_user_info(openid: str = Depends(get_current_user_openid)):
    mock_user = {
        "openid": openid,
        "nickname": "校园搭子用户",
        "avatar": "",
        "interest_tags": [],
        "create_time": "2026-11-05"
    }
    return {
        "code": 200,
        "msg": "查询成功",
        "data": mock_user
    }

@router.put("/info", summary="修改个人信息，需要登录态")
async def update_user_info(
    update_data: UserInfoUpdateRequest,
    openid: str = Depends(get_current_user_openid)
):
    return {
        "code": 200,
        "msg": "用户信息修改成功",
        "data": {
            "openid": openid,
            "update": update_data.dict(exclude_unset=True)
        }
    }
