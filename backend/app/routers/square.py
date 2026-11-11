"""邀约广场路由。"""


from fastapi import APIRouter, Query

from app.schemas.invitation import InvitationListResponse, InvitationType
from app.services import square_service

router = APIRouter(prefix="/api/invitations", tags=["square"])


@router.get("", response_model=InvitationListResponse)
def list_invitations(
    page: int = Query(default=1, ge=1, description="页码，从 1 开始"),
    page_size: int = Query(default=10, ge=1, le=50, description="每页数量，1-50"),
    inv_type: InvitationType | None = Query(default=None, alias="type"),
) -> InvitationListResponse:
    return square_service.list_invitations(page, page_size, inv_type)
