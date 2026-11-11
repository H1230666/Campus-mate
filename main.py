from fastapi import FastAPI
from pydantic import BaseModel
import uvicorn
from core.exception_handler import register_exception_handler
from core.exceptions import BusinessException, ErrorCode
import bcrypt

app = FastAPI(title="校园搭子小程序后端")
register_exception_handler(app)

# 密码哈希工具
def hash_password(raw_pwd: str) -> str:
    return bcrypt.hashpw(raw_pwd.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")

# 模拟用户库，密码都是哈希值，无明文
user_db = [
    {
        "id": 1,
        "account": "2026001",
        "password": hash_password("123456"),
        "nickname": "小搭子A"
    },
    {
        "id": 2,
        "account": "2026002",
        "password": hash_password("123456"),
        "nickname": "小搭子B"
    }
]

# 登录请求体
class LoginReq(BaseModel):
    account: str
    password: str

# 登录接口，错误统一抛 BusinessException
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

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
