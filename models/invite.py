from sqlalchemy import Column, Integer, String, Enum
from core.database import Base
import enum

class InviteStatus(str, enum.Enum):
    RECRUITING = "招募中"
    FULL = "已满"

class Invite(Base):
    __tablename__ = "invite"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    max_num = Column(Integer, comment="最大招募人数")
    current_num = Column(Integer, default=0, comment="当前已加入人数")
    status = Column(Enum(InviteStatus), default=InviteStatus.RECRUITING)
    creator_id = Column(Integer, comment="发布人ID")

class InviteJoin(Base):
    __tablename__ = "invite_join"
    id = Column(Integer, primary_key=True)
    invite_id = Column(Integer)
    user_id = Column(Integer)
