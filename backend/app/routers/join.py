"""报名加入邀约路由。"""

from fastapi import APIRouter, Depends, HTTPException, status

from app.core.auth import get_current_user_id
from app.repositories import invitation_repo
from app.schemas.invitation import InvitationOut

router = APIRouter(prefix="/api/invitations", tags=["join"])


@router.post("/{invitation_id}/join", response_model=InvitationOut, summary="报名加入邀约")
def join_invitation(
    invitation_id: int,
    user_id: int = Depends(get_current_user_id),
) -> InvitationOut:
    """报名成功返回更新后的邀约；邀约不存在返回 404，已满返回 400。"""
    invitation, error = invitation_repo.join_invitation(invitation_id, user_id)
    if invitation is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=error)
    if error is not None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)
    return invitation
