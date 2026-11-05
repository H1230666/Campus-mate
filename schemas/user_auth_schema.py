from pydantic import BaseModel, Field
from typing import List, Optional

# 微信登录请求：前端传微信code
class WxLoginRequest(BaseModel):
    code: str = Field(description="微信小程序前端拿到的code，用来换取openid")

# 修改用户信息请求
class UserInfoUpdateRequest(BaseModel):
    nickname: Optional[str] = Field(None, max_length=32, description="昵称")
    avatar: Optional[str] = Field(None, description="头像url")
    interest_tags: Optional[List[str]] = Field(None, description="兴趣标签列表")
