"""FastAPI 应用入口。"""

from fastapi import FastAPI

from app.routers import draft, publish, square, user

app = FastAPI(title="Campus-mate API", version="0.1.0-alpha")

# 注意注册顺序：/api/invitations/draft 必须先于 /api/invitations/{invitation_id}，
# 否则 "draft" 会被详情接口当成路径参数匹配。
app.include_router(publish.router)
app.include_router(draft.router)
app.include_router(square.router)
app.include_router(user.router)


@app.get("/health", tags=["meta"])
def health() -> dict:
    return {"status": "ok"}
