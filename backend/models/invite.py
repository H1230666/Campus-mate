from pydantic import BaseModel
from enum import Enum

class InviteStatus(str, Enum):
    RECRUITING = "recruiting"  # 招募中
    FULL = "full"              # 已满

class Invite(BaseModel):
    id: int
    title: str
    creator_id: int
    current_count: int
    max_count: int
    status: InviteStatus

class JoinInviteReq(BaseModel):
    invite_id: int
    user_id: int
