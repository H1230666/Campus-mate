"""草稿箱业务逻辑（issue #6）。"""

from app.repositories import invitation_repo
from app.schemas.invitation import InvitationDraftIn, InvitationDraftOut


def save_draft(publisher_id: int, payload: InvitationDraftIn) -> InvitationDraftOut:
    return invitation_repo.save_draft(publisher_id, payload)


def get_draft(publisher_id: int) -> InvitationDraftOut | None:
    return invitation_repo.get_draft(publisher_id)


def discard_draft(publisher_id: int) -> bool:
    """丢弃草稿；草稿不存在时也返回成功，保证重复点击不报错。"""
    return invitation_repo.clear_draft(publisher_id)
