"""用户表 ORM 模型。"""

from sqlalchemy import Column, DateTime, Integer, String, func
from sqlalchemy.orm import declarative_base

Base = declarative_base()


class User(Base):
    """用户表：id / 微信 openid / 昵称 / 头像 / 兴趣标签 / 创建时间。"""

    __tablename__ = "user"

    id = Column(Integer, primary_key=True, autoincrement=True, comment="主键 id")
    openid = Column(String(64), nullable=False, unique=True, index=True, comment="微信 openid")
    nickname = Column(String(32), nullable=False, comment="昵称")
    avatar = Column(String(255), nullable=True, comment="头像 url")
    interest_tag = Column(String(128), nullable=True, comment="兴趣标签，逗号分隔")
    create_time = Column(DateTime, nullable=False, default=func.now(), comment="创建时间")

    def __repr__(self) -> str:
        return f"<User id={self.id} nickname={self.nickname!r}>"
