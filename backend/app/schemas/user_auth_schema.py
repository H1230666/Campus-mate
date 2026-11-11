"""登录与用户信息相关入参。"""


from pydantic import BaseModel, Field


class WxLoginRequest(BaseModel):
    """微信登录：前端通过 wx.login 拿到 code。"""

    code: str = Field(min_length=1, description="微信小程序前端拿到的 code，用于换取 openid")


class UserInfoUpdateRequest(BaseModel):
    """修改个人信息入参，全部可选。"""

    nickname: str | None = Field(default=None, max_length=32, description="昵称")
    avatar: str | None = Field(default=None, max_length=255, description="头像 url")
    interest_tags: list[str] | None = Field(default=None, description="兴趣标签列表")
