import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))

from pydantic import ValidationError
from schemas.user_schema import UserCreate, UserUpdate

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
    try:
        UserCreate(username="ab", password="123456")
        assert False
    except ValidationError:
        assert True

def test_user_create_password_too_short():
    """密码太短校验失败"""
    try:
        UserCreate(username="student02", password="123")
        assert False
    except ValidationError:
        assert True

def test_user_update_info():
    """测试更新昵称"""
    update = UserUpdate(nickname="新昵称")
    assert update.nickname == "新昵称"
