"""邀约（搭子）模块的数据模型与查询参数。"""

from datetime import UTC, datetime, timedelta
from enum import Enum
from typing import Annotated

from pydantic import BaseModel, Field, StringConstraints, field_validator

#: 最多允许提前多少天发布邀约
MAX_AHEAD_DAYS = 30


class InvitationType(str, Enum):
    """搭子类型。"""

    STUDY = "study"
    SPORT = "sport"
    FOOD = "food"
    TRAVEL = "travel"
    OTHER = "other"


class InvitationStatus(str, Enum):
    """邀约状态：招募中 / 已满。"""

    RECRUITING = "recruiting"
    FULL = "full"


class InvitationOut(BaseModel):
    """邀约列表与详情返回结构。"""

    id: int
    title: str
    type: InvitationType
    location: str
    start_time: datetime
    current_count: int = Field(ge=0)
    max_count: int = Field(ge=1)
    status: InvitationStatus
    publisher_id: int
    description: str | None = None
    created_at: datetime


class InvitationListQuery(BaseModel):
    """广场列表查询参数：分页 + 类型筛选。"""

    page: int = Field(default=1, ge=1)
    page_size: int = Field(default=10, ge=1, le=50)
    type: InvitationType | None = None


class InvitationListResponse(BaseModel):
    """广场分页列表响应。"""

    total: int
    page: int
    page_size: int
    list: list[InvitationOut]


# ---------- 发布与草稿（issue #5 / #6） ----------

TitleText = Annotated[
    str, StringConstraints(strip_whitespace=True, min_length=4, max_length=30)
]
LocationText = Annotated[
    str, StringConstraints(strip_whitespace=True, min_length=2, max_length=50)
]
DescriptionText = Annotated[str, StringConstraints(strip_whitespace=True, max_length=500)]

#: 草稿允许字段为空，只限制长度，不做必填校验
DraftTitleText = Annotated[str, StringConstraints(strip_whitespace=True, max_length=30)]
DraftLocationText = Annotated[str, StringConstraints(strip_whitespace=True, max_length=50)]


class InvitationCreate(BaseModel):
    """发布邀约请求体。

    只接收用户可填字段；status / current_count / publisher_id 由服务端决定，
    避免客户端伪造“已满”状态或冒充他人发布。
    """

    title: TitleText
    type: InvitationType
    location: LocationText
    start_time: datetime
    max_count: int = Field(ge=2, le=20, description="招募人数上限，2-20 人")
    description: DescriptionText | None = Field(default=None, description="补充说明，最多 500 字")

    @field_validator("start_time")
    @classmethod
    def validate_start_time(cls, value: datetime) -> datetime:
        """开始时间必须晚于当前时间，且最多提前 30 天。"""
        start = value if value.tzinfo is not None else value.replace(tzinfo=UTC)
        now = datetime.now(UTC)
        if start <= now:
            raise ValueError("开始时间必须晚于当前时间")
        if start > now + timedelta(days=MAX_AHEAD_DAYS):
            raise ValueError(f"开始时间最多提前 {MAX_AHEAD_DAYS} 天")
        return start.astimezone(UTC)


class InvitationDraftIn(BaseModel):
    """草稿保存请求体：所有字段可选，允许用户只填一半就退出。"""

    title: DraftTitleText | None = None
    type: InvitationType | None = None
    location: DraftLocationText | None = None
    start_time: datetime | None = None
    max_count: int | None = Field(default=None, ge=2, le=20)
    description: DescriptionText | None = None


class InvitationDraftOut(InvitationDraftIn):
    """草稿返回结构，额外带上服务端保存时间。"""

    updated_at: datetime
