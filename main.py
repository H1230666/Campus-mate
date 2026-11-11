from fastapi import FastAPI
from pydantic import BaseModel
import uvicorn
from core.exception_handler import register_exception_handler
from core.exceptions import BusinessException, ErrorCode
import bcrypt

app = FastAPI(title="校园搭子小程序后端")
register_exception_handler(app)
 
# 固定哈希，明文都是123456，不再动态生成
user_db = [
    {
        "id": 1,
        "account": "2026001",
        "password": "$2b$12$EixZaYb3G7pRk0H0uH0R5eO27w05gFzRb9H1u03n0G0tG7sG0l0q",
        "nickname": "小搭子A"
    },
    {
        "id": 2,
        "account": "2026002",
        "password": "$2b$12$EixZaYb3G7pRk0H0uH0R5eO27w05gFzRb9H1u03n0G0tG7sG0l0q",
        "nickname": "小搭子B"
    }
]

# 账号密码登录请求体
class LoginReq(BaseModel):
    account: str
    password: str

# 微信登录请求体
class WxLoginBody(BaseModel):
    code: str

# 账号密码登录接口
@app.post("/account/login")
async def account_login(req: LoginReq):
    user = next((u for u in user_db if u["account"] == req.account), None)
    if not user:
        raise BusinessException(ErrorCode.LOGIN_FAILED, "账号不存在")
    if not bcrypt.checkpw(req.password.encode("utf-8"), user["password"].encode("utf-8")):
        raise BusinessException(ErrorCode.LOGIN_FAILED, "账号或密码错误")

    return {
        "id": user["id"],
        "account": user["account"],
        "nickname": user["nickname"]
    }

# 微信登录接口（改造：不用return 400，统一抛异常）
@app.post("/login")
def wx_login(body: WxLoginBody):
    if not body.code:
        raise BusinessException(ErrorCode.LOGIN_FAILED, "code无效")
    return {
        "code": 200,
        "msg": "微信登录成功",
        "data": {"openid": "mock_openid_123456", "nickname": "微信用户"}
    }

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
