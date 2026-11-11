from threading import Lock

from backend.models.invite import Invite, InviteStatus, JoinInviteReq
from fastapi import APIRouter, HTTPException

router = APIRouter(prefix="/invite", tags=["邀约"])

# 模拟数据库，真实项目替换成db
invite_db: dict[int, Invite] = {
    1: Invite(id=1, title="一起去图书馆", creator_id=1, current_count=1, max_count=3, status=InviteStatus.RECRUITING)
}

invite_lock = Lock()

@router.post("/join")
def join_invite(req: JoinInviteReq):
    with invite_lock:
        invite = invite_db.get(req.invite_id)
        if not invite:
            raise HTTPException(status_code=404, detail="邀约不存在")

        if invite.status == InviteStatus.FULL:
            raise HTTPException(status_code=400, detail="邀约已满，无法加入")

        if invite.current_count >= invite.max_count:
            invite.status = InviteStatus.FULL
            raise HTTPException(status_code=400, detail="名额已满")

        # 人数+1
        invite.current_count += 1

        # 满了自动切换状态
        if invite.current_count >= invite.max_count:
            invite.status = InviteStatus.FULL

        return {
            "ok": True,
            "invite": invite.model_dump()
        }

@router.get("/{invite_id}")
def get_invite(invite_id: int):
    invite = invite_db.get(invite_id)
    if not invite:
        raise HTTPException(status_code=404, detail="邀约不存在")
    return invite.model_dump()
