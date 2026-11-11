"""用户表 ORM 模型。"""

from sqlalchemy import Boolean, Column, DateTime, Integer, String, func
from sqlalchemy.orm import declarative_base

Base = declarative_base()


class User(Base):
    """用户表：账号 / 密码哈希 / 微信 openid / 昵称 / 头像 / 兴趣标签 / 状态 / 时间。"""

    __tablename__ = "user"

    id = Column(Integer, primary_key=True, autoincrement=True, comment="主键 id")
    username = Column(String(20), nullable=False, unique=True, index=True, comment="登录用户名")
    password_hash = Column(
        String(255),
        nullable=False,
        comment="密码哈希（bcrypt/pbkdf2），任何情况下都不保存明文",
    )
    openid = Column(
        String(64),
        nullable=True,
        unique=True,
        index=True,
        comment="微信 openid，账号密码注册用户可为空",
    )
    nickname = Column(String(32), nullable=False, comment="昵称")
    phone = Column(String(11), nullable=True, index=True, comment="手机号")
    avatar = Column(String(255), nullable=True, comment="头像 url")
    interest_tag = Column(String(128), nullable=True, comment="兴趣标签，逗号分隔")
    is_active = Column(Boolean, nullable=False, default=True, comment="是否启用，仅管理员可改")
    create_time = Column(DateTime, nullable=False, default=func.now(), comment="创建时间")
    update_time = Column(
        DateTime,
        nullable=False,
        default=func.now(),
        onupdate=func.now(),
        comment="更新时间",
    )

    def __repr__(self) -> str:
        return f"<User id={self.id} username={self.username!r}>"
