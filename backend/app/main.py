"""FastAPI 应用入口。"""

from fastapi import FastAPI

from app.core.exception_handler import register_exception_handler
from app.routers import draft, join, publish, square, user

app = FastAPI(title="Campus-mate API", version="0.1.0-alpha")

# 统一错误响应体：业务异常 / 校验异常 / HTTP 异常 / 未捕获异常
register_exception_handler(app)

# 注意注册顺序：/api/invitations/draft 必须先于 /api/invitations/{invitation_id}，
# 否则 "draft" 会被详情接口当成路径参数匹配。
app.include_router(publish.router)
app.include_router(draft.router)
app.include_router(square.router)
app.include_router(join.router)
app.include_router(user.router)


@app.get("/health", tags=["meta"])
def health() -> dict:
    return {"status": "ok"}
