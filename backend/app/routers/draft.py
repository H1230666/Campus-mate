"""草稿箱路由（issue #6）。"""

from fastapi import APIRouter, Depends, Response, status

from app.core.auth import get_current_user_id
from app.schemas.invitation import InvitationDraftIn, InvitationDraftOut
from app.services import draft_service

router = APIRouter(prefix="/api/invitations/draft", tags=["draft"])


@router.get("", response_model=InvitationDraftOut | None, summary="获取当前草稿")
def get_draft(publisher_id: int = Depends(get_current_user_id)) -> InvitationDraftOut | None:
    """返回当前用户草稿；没有草稿时返回 null，前端据此决定是否恢复表单。"""
    return draft_service.get_draft(publisher_id)


@router.put("", response_model=InvitationDraftOut, summary="保存当前草稿")
def save_draft(
    payload: InvitationDraftIn,
    publisher_id: int = Depends(get_current_user_id),
) -> InvitationDraftOut:
    """部分字段更新：未提交的字段保留上一次保存的值。"""
    return draft_service.save_draft(publisher_id, payload)


@router.delete("", status_code=status.HTTP_204_NO_CONTENT, summary="丢弃当前草稿")
def discard_draft(publisher_id: int = Depends(get_current_user_id)) -> Response:
    """删除草稿；草稿不存在时同样返回 204（幂等）。"""
    draft_service.discard_draft(publisher_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
