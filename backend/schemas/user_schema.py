from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional

class UserCreate(BaseModel):
    username: str = Field(min_length=3, max_length=50, description="用户名，3-50字符")
    password: str = Field(min_length=6, max_length=100, description="密码，最少6位")
    nickname: Optional[str] = Field(default=None, max_length=50, description="昵称")
    phone: Optional[str] = Field(default=None, max_length=20, description="手机号")
    avatar: Optional[str] = Field(default=None, max_length=255, description="头像链接")

class UserUpdate(BaseModel):
    nickname: Optional[str] = Field(default=None, max_length=50)
    phone: Optional[str] = Field(default=None, max_length=20)
    avatar: Optional[str] = Field(default=None, max_length=255)
    is_active: Optional[bool] = Field(default=None)

class UserResponse(BaseModel):
    id: int
    username: str
    nickname: Optional[str]
    phone: Optional[str]
    avatar: Optional[str]
    is_active: bool
    create_time: datetime
    update_time: datetime

    model_config = {
        "from_attributes": True
    }
