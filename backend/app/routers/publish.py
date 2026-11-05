"""邀约发布路由（issue #5）。"""

from fastapi import APIRouter, Depends, status

from app.core.auth import get_current_user_id
from app.schemas.invitation import InvitationCreate, InvitationOut
from app.services import publish_service

router = APIRouter(prefix="/api/invitations", tags=["publish"])


@router.post(
    "",
    response_model=InvitationOut,
    status_code=status.HTTP_201_CREATED,
    summary="发布搭子邀约",
)
def publish_invitation(
    payload: InvitationCreate,
    publisher_id: int = Depends(get_current_user_id),
) -> InvitationOut:
    """发布一条招募中的邀约，发布成功后清空当前草稿。"""
    return publish_service.publish(payload, publisher_id)
