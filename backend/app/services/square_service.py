"""邀约广场业务逻辑。"""


from app.repositories.invitation_repo import get_invitation as repo_get
from app.repositories.invitation_repo import list_invitations as repo_list
from app.schemas.invitation import (
    InvitationListResponse,
    InvitationOut,
    InvitationStatus,
    InvitationType,
)


def list_invitations(
    page: int,
    page_size: int,
    inv_type: InvitationType | None,
    inv_status: InvitationStatus | None = None,
) -> InvitationListResponse:
    total, items = repo_list(page, page_size, inv_type, inv_status)
    return InvitationListResponse(
        total=total, page=page, page_size=page_size, list=items
    )


def get_invitation(invitation_id: int) -> InvitationOut | None:
    return repo_get(invitation_id)
