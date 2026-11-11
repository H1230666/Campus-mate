"""FastAPI 应用入口。"""

from fastapi import FastAPI

from app.routers import square, user

app = FastAPI(title="Campus-mate API", version="0.1.0-alpha")
app.include_router(square.router)
app.include_router(user.router)


@app.get("/health", tags=["meta"])
def health() -> dict:
    return {"status": "ok"}
