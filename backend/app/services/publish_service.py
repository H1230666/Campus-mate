"""邀约发布业务逻辑（issue #5）。"""

from app.repositories import invitation_repo
from app.schemas.invitation import InvitationCreate, InvitationOut


def publish(payload: InvitationCreate, publisher_id: int) -> InvitationOut:
    """发布邀约：状态、当前人数、创建时间均由仓储层按服务端规则赋值。"""
    return invitation_repo.create_invitation(payload, publisher_id)
