import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent.parent.parent))
import pytest
from pydantic import ValidationError
from backend.app.schemas.user_schema import UserCreate, UserUpdate


def test_user_create_valid():
    """测试合法用户创建"""
    user = UserCreate(
        username="student01",
        password="123456",
        nickname="小搭子",
        phone="13800138000"
    )
    assert user.username == "student01"
    assert user.password == "123456"


def test_user_create_username_too_short():
    """用户名太短校验失败"""
    with pytest.raises(ValidationError):
        UserCreate(username="ab", password="123456")


def test_user_create_password_too_short():
    """密码太短校验失败"""
    with pytest.raises(ValidationError):
        UserCreate(username="student02", password="123")


def test_user_update_info():
    """测试更新昵称"""
    update = UserUpdate(nickname="新昵称")
    assert update.nickname == "新昵称"
