"""登录态依赖。

Alpha 阶段登录接口（issue #2）尚未合入，这里先用 ``X-User-Id`` 请求头
作为临时身份来源，保证发布/草稿接口可以独立开发与联调。

待 #2 合入后，只需把本函数替换为「解析 Bearer Token 并返回 user_id」，
路由层与服务层不需要改动。
"""

from fastapi import Header, HTTPException, status


def get_current_user_id(
    x_user_id: int | None = Header(default=None, alias="X-User-Id"),
) -> int:
    """从请求头取当前用户 id；缺失或非法时返回 401。"""
    if x_user_id is None or x_user_id <= 0:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="未登录：缺少有效的 X-User-Id",
        )
    return x_user_id
