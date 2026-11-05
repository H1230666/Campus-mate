"""邀约发布业务逻辑（issue #5）。"""

from app.repositories import invitation_repo
from app.schemas.invitation import InvitationCreate, InvitationOut


def publish(payload: InvitationCreate, publisher_id: int) -> InvitationOut:
    """发布邀约。

    发布成功后清空该用户的服务端草稿，避免“已发布但仍提示继续编辑”的脏状态。
    """
    invitation = invitation_repo.create_invitation(payload, publisher_id)
    invitation_repo.clear_draft(publisher_id)
    return invitation
