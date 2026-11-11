from sqlalchemy import Column, Integer, String, DateTime, func
from sqlalchemy.orm import declarative_base

Base = declarative_base()

class User(Base):
    __tablename__ = "user"
    id = Column(Integer, primary_key=True, autoincrement=True, comment="主键id")
    openid = Column(String(64), nullable=False, comment="微信openid")
    nickname = Column(String(32), nullable=False, comment="昵称")
    avatar = Column(String(255), nullable=True, comment="头像url")
    interest_tag = Column(String(128), nullable=True, comment="兴趣标签，逗号分隔")
    create_time = Column(DateTime, default=func.now(), comment="创建时间")
