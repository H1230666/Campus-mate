from enum import Enum

class ErrorCode(int, Enum):
    SUCCESS = 0
    BAD_REQUEST = 400
    PARAM_VALIDATE_ERROR = 40001
    NOT_FOUND = 404
    INTERNAL_ERROR = 50001
    LOGIN_FAILED = 10001
    
class BusinessException(Exception):
    def __init__(self, code: ErrorCode, msg: str):
        self.code = code
        self.msg = msg
