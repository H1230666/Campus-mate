from fastapi import FastAPI
from pydantic import BaseModel
import uvicorn
from core.exception_handler import register_exception_handler

app = FastAPI(title="校园搭子小程序后端")
register_exception_handler(app)
# 内存模拟用户表
user_db = [
    {"id": 1, "account": "2026001", "password": "123456", "nickname": "小搭子A"},
    {"id": 2, "account": "2026002", "password": "123456", "nickname": "小搭子B"},
]

# 微信登录请求体
class WxLoginBody(BaseModel):
    code: str

# 账号密码登录请求体
class AccountLoginBody(BaseModel):
    account: str
    password: str


@app.post("/login")
def wx_login(body: WxLoginBody):
    """微信一键登录接口"""
    # 真实项目这里要调用微信接口拿 openid，作业我们直接模拟
    if not body.code:
        return {"code": 400, "msg": "code无效"}
    return {
        "code": 200,
        "msg": "微信登录成功",
        "data": {"openid": "mock_openid_123456", "nickname": "微信用户"}
    }


@app.post("/account-login")
def account_login(body: AccountLoginBody):
    """学号/手机号+密码登录接口"""
    for u in user_db:
        if u["account"] == body.account and u["password"] == body.password:
            return {
                "code": 200,
                "msg": "登录成功",
                "data": {"uid": u["id"], "account": u["account"], "nickname": u["nickname"]}
            }
    return {"code": 401, "msg": "学号或密码错误"}


if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
