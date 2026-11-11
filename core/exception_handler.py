from fastapi import Request, FastAPI
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException
from .exceptions import BusinessException, ErrorCode
import logging

logger = logging.getLogger(__name__)


def register_exception_handler(app: FastAPI):
    # 业务自定义异常
    @app.exception_handler(BusinessException)
    async def business_exception_handler(request: Request, exc: BusinessException):
        return JSONResponse(
            status_code=200,
            content={
                "code": exc.code,
                "msg": exc.msg,
                "data": None
            }
        )

 # 参数校验异常
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    return JSONResponse(
        status_code=422,
        content={
            "code": ErrorCode.PARAM_VALIDATE_ERROR,
            "msg": "参数校验失败",
            "data": exc.errors()
        }
    )

# HTTP异常
@app.exception_handler(StarletteHTTPException)
async def http_exception_handler(request: Request, exc: StarletteHTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "code": exc.status_code,
            "msg": exc.detail,
            "data": None
        }
    )





# 全局兜底未知异常
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    # 打印完整堆栈到日志
    logger.exception("服务器未知异常")
    # 这里你可以用环境变量判断DEBUG，先写简易版本
    return JSONResponse(
        status_code=500,
        content={
            "code": ErrorCode.INTERNAL_ERROR,
            "msg": "服务器内部异常",
            "data": None
        }
    )
