"""邀约数据访问层。

当前使用进程内列表作为占位存储，便于中期联调与测试。
后续替换为 MySQL（SQLAlchemy）时只需保持本模块对外接口不变：
    list_invitations(page, page_size, inv_type) -> (total, items)
    get_invitation(invitation_id) -> Optional[InvitationOut]
"""

from datetime import UTC, datetime, timedelta

from app.schemas.invitation import InvitationOut, InvitationStatus, InvitationType


def _dt(days_ago: int, hour: int) -> datetime:
    base = datetime.now(UTC).replace(microsecond=0) - timedelta(days=days_ago)
    return base.replace(hour=hour)


_SEED = [
    InvitationOut(
        id=1,
        title="图书馆自习搭子",
        type=InvitationType.STUDY,
        location="图书馆三楼自习区",
        start_time=_dt(0, 9),
        current_count=2,
        max_count=4,
        status=InvitationStatus.RECRUITING,
        publisher_id=101,
        description="一起备考六级，互相监督。",
        created_at=_dt(2, 20),
    ),
    InvitationOut(
        id=2,
        title="羽毛球约球",
        type=InvitationType.SPORT,
        location="东区体育馆",
        start_time=_dt(1, 19),
        current_count=4,
        max_count=4,
        status=InvitationStatus.FULL,
        publisher_id=102,
        description="双打还差一位，水平不限。",
        created_at=_dt(2, 18),
    ),
    InvitationOut(
        id=3,
        title="食堂拼饭",
        type=InvitationType.FOOD,
        location="二食堂二楼",
        start_time=_dt(0, 12),
        current_count=1,
        max_count=3,
        status=InvitationStatus.RECRUITING,
        publisher_id=103,
        description="新开的麻辣香锅，来两个饭搭子。",
        created_at=_dt(1, 21),
    ),
    InvitationOut(
        id=4,
        title="周末爬山",
        type=InvitationType.TRAVEL,
        location="校门口集合",
        start_time=_dt(3, 8),
        current_count=3,
        max_count=6,
        status=InvitationStatus.RECRUITING,
        publisher_id=104,
        description="周末郊外徒步，AA 拼车。",
        created_at=_dt(1, 17),
    ),
    InvitationOut(
        id=5,
        title="算法刷题小组",
        type=InvitationType.STUDY,
        location="一教 204",
        start_time=_dt(0, 15),
        current_count=5,
        max_count=5,
        status=InvitationStatus.FULL,
        publisher_id=105,
        description="LeetCode 每日一题。",
        created_at=_dt(0, 22),
    ),
    InvitationOut(
        id=6,
        title="夜跑五公里",
        type=InvitationType.SPORT,
        location="西操场",
        start_time=_dt(0, 21),
        current_count=2,
        max_count=8,
        status=InvitationStatus.RECRUITING,
        publisher_id=106,
        description="配速 6 分半，轻松跑。",
        created_at=_dt(0, 20),
    ),
    InvitationOut(
        id=7,
        title="奶茶探店",
        type=InvitationType.FOOD,
        location="北门商业街",
        start_time=_dt(1, 16),
        current_count=2,
        max_count=4,
        status=InvitationStatus.RECRUITING,
        publisher_id=107,
        description="新店开业，第二杯半价。",
        created_at=_dt(0, 18),
    ),
    InvitationOut(
        id=8,
        title="校园摄影扫街",
        type=InvitationType.OTHER,
        location="樱花大道",
        start_time=_dt(2, 10),
        current_count=1,
        max_count=3,
        status=InvitationStatus.RECRUITING,
        publisher_id=108,
        description="互相当模特，手机相机皆可。",
        created_at=_dt(0, 16),
    ),
]

_INVITATIONS: list[InvitationOut] = sorted(
    _SEED, key=lambda item: item.created_at, reverse=True
)


def list_invitations(
    page: int,
    page_size: int,
    inv_type: InvitationType | None,
    inv_status: InvitationStatus | None = None,
) -> tuple[int, list[InvitationOut]]:
    """返回可见邀约（招募中/已满）的分页结果与总数。"""
    visible = [
        item
        for item in _INVITATIONS
        if item.status in (InvitationStatus.RECRUITING, InvitationStatus.FULL)
    ]
    if inv_type is not None:
        visible = [item for item in visible if item.type == inv_type]
    if inv_status is not None:
        visible = [item for item in visible if item.status == inv_status]
    total = len(visible)
    start = (page - 1) * page_size
    return total, visible[start : start + page_size]


def get_invitation(invitation_id: int) -> InvitationOut | None:
    """按 id 查询单条邀约，不存在时返回 None。"""
    for item in _INVITATIONS:
        if item.id == invitation_id:
            return item
    return None
