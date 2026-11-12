"""统一错误码与业务异常。

Alpha 阶段错误响应体统一为 ``{"code": int, "msg": str, "data": Any}``，
由 ``app.core.exception_handler`` 中的全局处理器负责转换。
"""

from enum import Enum


class ErrorCode(int, Enum):
    """业务错误码：0 表示成功，其余按段划分，避免与 HTTP 状态码混淆。"""

    SUCCESS = 0
    BAD_REQUEST = 400
    UNAUTHORIZED = 401
    NOT_FOUND = 404
    PARAM_VALIDATE_ERROR = 40001
    INTERNAL_ERROR = 50001


class BusinessException(Exception):
    """业务侧可预期异常，抛出后由全局异常处理器转成标准错误响应。

    Args:
        code: 业务错误码，默认取对应 HTTP 状态码。
        msg: 面向用户的错误提示。
        status_code: 响应 HTTP 状态码；缺省时使用 ``code`` 的数值。
    """

    def __init__(
        self, code: ErrorCode, msg: str, status_code: int | None = None
    ) -> None:
        self.code = code
        self.msg = msg
        self.status_code = status_code if status_code is not None else code.value
