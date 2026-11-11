"""邀约（搭子）模块的数据模型与查询参数。"""

from datetime import datetime
from enum import Enum

from pydantic import BaseModel, Field


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
