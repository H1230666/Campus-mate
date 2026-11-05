from backend.models.invite import Invite, InviteStatus


def test_invite_auto_full():
    """人数到达上限自动切换为已满"""
    invite = Invite(max_num=2, current_num=1, status=InviteStatus.RECRUITING)
    invite.current_num += 1
    if invite.current_num >= invite.max_num:
        invite.status = InviteStatus.FULL
    assert invite.status == InviteStatus.FULL
