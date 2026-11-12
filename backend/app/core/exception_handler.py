"""全局异常处理器注册。

把业务异常、参数校验异常、HTTP 异常与未捕获异常统一转换为
``{"code", "msg", "data"}`` 结构；未捕获异常记录日志后返回 500，
避免直接回显调试堆栈。
"""

import logging

from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from starlette.exceptions import HTTPException as StarletteHTTPException

from app.core.exceptions import BusinessException, ErrorCode

logger = logging.getLogger(__name__)


def _error_body(code: int, msg: str, data: object = None) -> dict:
    return {"code": code, "msg": msg, "data": data}


def _sanitize_validation_errors(errors: list[dict]) -> list[dict]:
    """清洗 Pydantic 校验错误：剔除不可序列化的异常对象，ctx 一律转字符串。"""
    cleaned: list[dict] = []
    for err in errors:
        item: dict = {
            "loc": list(err.get("loc", [])),
            "msg": err.get("msg", ""),
            "type": err.get("type", ""),
        }
        ctx = err.get("ctx")
        if ctx:
            item["ctx"] = {key: str(value) for key, value in ctx.items()}
        cleaned.append(item)
    return cleaned


def register_exception_handler(app: FastAPI) -> None:
    """在应用上注册四类全局异常处理器。"""

    @app.exception_handler(BusinessException)
    async def _business_exception_handler(
        _: Request, exc: BusinessException
    ) -> JSONResponse:
        return JSONResponse(
            status_code=exc.status_code,
            content=_error_body(exc.code.value, exc.msg),
        )

    @app.exception_handler(RequestValidationError)
    async def _validation_exception_handler(
        _: Request, exc: RequestValidationError
    ) -> JSONResponse:
        return JSONResponse(
            status_code=422,
            content=_error_body(
                ErrorCode.PARAM_VALIDATE_ERROR.value,
                "参数校验失败",
                _sanitize_validation_errors(exc.errors()),
            ),
        )

    @app.exception_handler(StarletteHTTPException)
    async def _http_exception_handler(
        _: Request, exc: StarletteHTTPException
    ) -> JSONResponse:
        return JSONResponse(
            status_code=exc.status_code,
            content=_error_body(exc.status_code, str(exc.detail)),
        )

    @app.exception_handler(Exception)
    async def _unhandled_exception_handler(
        _: Request, exc: Exception
    ) -> JSONResponse:
        logger.exception("未捕获的服务器异常: %s", exc)
        return JSONResponse(
            status_code=500,
            content=_error_body(ErrorCode.INTERNAL_ERROR.value, "服务器内部异常"),
        )
