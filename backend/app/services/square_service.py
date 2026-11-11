"""邀约广场业务逻辑。"""


from app.repositories.invitation_repo import list_invitations as repo_list
from app.schemas.invitation import InvitationListResponse, InvitationType


def list_invitations(
    page: int, page_size: int, inv_type: InvitationType | None
) -> InvitationListResponse:
    total, items = repo_list(page, page_size, inv_type)
    return InvitationListResponse(
        total=total, page=page, page_size=page_size, list=items
    )
