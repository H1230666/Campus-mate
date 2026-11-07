"""用户模块 Pydantic 模型。"""

import re
from datetime import datetime

from pydantic import BaseModel, Field, field_validator

USERNAME_PATTERN = re.compile(r"^[A-Za-z0-9_]+$")
PHONE_PATTERN = re.compile(r"^1[3-9]\d{9}$")


class UserCreate(BaseModel):
    """用户注册入参：长度与格式统一在此校验，避免脏数据入库。"""

    username: str = Field(min_length=3, max_length=20, description="用户名，3-20 个字符，仅字母/数字/下划线")
    password: str = Field(min_length=6, max_length=32, description="密码，6-32 个字符，首尾不能有空格")
    nickname: str | None = Field(default=None, max_length=32, description="昵称")
    phone: str | None = Field(default=None, description="手机号，11 位，1 开头")
    avatar: str | None = Field(default=None, max_length=255, description="头像链接")

    @field_validator("username")
    @classmethod
    def check_username(cls, v: str) -> str:
        if not USERNAME_PATTERN.fullmatch(v):
            raise ValueError("用户名只能包含字母、数字和下划线")
        return v

    @field_validator("password")
    @classmethod
    def check_password(cls, v: str) -> str:
        if v != v.strip():
            raise ValueError("密码首尾不能包含空格")
        return v

    @field_validator("phone")
    @classmethod
    def check_phone(cls, v: str | None) -> str | None:
        if v is None or v == "":
            return None
        if not PHONE_PATTERN.fullmatch(v):
            raise ValueError("手机号格式不正确，应为 11 位且以 1 开头")
        return v

    @field_validator("nickname")
    @classmethod
    def check_nickname(cls, v: str | None) -> str | None:
        if v is not None and v.strip() == "":
            raise ValueError("昵称不能为空白字符串")
        return v


class UserUpdate(BaseModel):
    """用户信息修改入参：全部可选，仅允许修改下列字段。"""

    nickname: str | None = Field(default=None, max_length=32, description="昵称")
    phone: str | None = Field(default=None, description="手机号，11 位，1 开头")
    avatar: str | None = Field(default=None, max_length=255, description="头像链接")
    is_active: bool | None = Field(default=None, description="是否启用")

    @field_validator("phone")
    @classmethod
    def check_phone(cls, v: str | None) -> str | None:
        if v is None or v == "":
            return None
        if not PHONE_PATTERN.fullmatch(v):
            raise ValueError("手机号格式不正确，应为 11 位且以 1 开头")
        return v


class UserResponse(BaseModel):
    """用户信息出参：可直接由 ORM 对象转换。"""

    id: int
    username: str
    nickname: str | None
    phone: str | None
    avatar: str | None
    is_active: bool
    create_time: datetime
    update_time: datetime

    model_config = {"from_attributes": True}
