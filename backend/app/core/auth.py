"""登录态依赖。

Alpha 阶段登录接口（issue #2）尚未合入，这里先用 ``X-User-Id`` 请求头
作为临时身份来源，保证发布/草稿接口可以独立开发与联调。

⚠️ TODO(#2): 登录接口合入后，本函数必须改为解析
``Authorization: Bearer <token>`` 并返回真实 user_id，随后删除 X-User-Id 分支。
在此之前，非 dev/test 环境会直接拒绝该头，避免可伪造身份被带上生产。
"""

import os

from fastapi import Header, HTTPException, status

APP_ENV = os.getenv("APP_ENV", "dev").strip().lower()


def get_current_user_id(
    x_user_id: int | None = Header(default=None, alias="X-User-Id"),
) -> int:
    """从请求头取当前用户 id；缺失或非法时返回 401。

    仅 dev/test 环境可用，其余环境返回 501，等待 #2 的 Bearer Token 接入。
    """
    if APP_ENV not in ("dev", "test"):
        raise HTTPException(
            status_code=status.HTTP_501_NOT_IMPLEMENTED,
            detail="X-User-Id 仅开发环境可用，请使用 Authorization: Bearer <token>",
        )
    if x_user_id is None or x_user_id <= 0:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="未登录：缺少有效的 X-User-Id",
        )
    return x_user_id
