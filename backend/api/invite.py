from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from backend.models.invite import Invite, InviteJoin, InviteStatus
from backend.core.deps import get_current_user, CurrentUser
from backend.core.database import get_db

router = APIRouter(prefix="/invite", tags=["邀约模块"])

@router.post("/{invite_id}/join")
def join_invite(
    invite_id: int,
    db: Session = Depends(get_db),
    user: CurrentUser = Depends(get_current_user)
):
    invite = db.query(Invite).filter(Invite.id == invite_id).first()
    if not invite:
        raise HTTPException(status_code=404, detail="邀约不存在")

    if invite.status == InviteStatus.FULL:
        raise HTTPException(status_code=400, detail="邀约人数已满，无法加入")

    exist_join = db.query(InviteJoin).filter(
        InviteJoin.invite_id == invite_id,
        InviteJoin.user_id == user.id
    ).first()
    if exist_join:
        raise HTTPException(status_code=400, detail="你已经加入该邀约")

    new_join = InviteJoin(invite_id=invite_id, user_id=user.id)
    db.add(new_join)
    invite.current_num += 1

    if invite.current_num >= invite.max_num:
        invite.status = InviteStatus.FULL

    db.commit()
    return {
        "code": 200,
        "msg": "加入搭子成功",
        "data": {
            "invite_id": invite.id,
            "current_num": invite.current_num,
            "max_num": invite.max_num,
            "status": invite.status
        }
    }

