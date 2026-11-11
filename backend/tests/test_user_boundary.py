"""用户模型边界用例：正常值 / 边界值 / 非法值。

对应 Issue #1 验收标准：字段非空、长度校验，单测用例 >= 1。
"""

import pytest
from pydantic import ValidationError

from app.schemas.user_schema import UserCreate, UserUpdate


def _create(**kwargs):
    base = dict(username="student01", password="abc123")
    base.update(kwargs)
    return UserCreate(**base)


def test_username_boundary_length():
    """用户名 3-20 个字符：20 个合法，21 个越界。"""
    assert _create(username="a" * 20).username == "a" * 20
    with pytest.raises(ValidationError):
        _create(username="a" * 21)


def test_username_rejects_chinese_and_space():
    """用户名只允许字母、数字、下划线。"""
    with pytest.raises(ValidationError):
        _create(username="张三")
    with pytest.raises(ValidationError):
        _create(username="student 01")


def test_password_boundary_length():
    """密码 6-32 个字符：6 个合法，5 个越界。"""
    assert _create(password="a1b2c3").password == "a1b2c3"
    with pytest.raises(ValidationError):
        _create(password="a1b2c")


def test_password_rejects_surrounding_space():
    """密码首尾不能有空格，避免登录时无法复现。"""
    with pytest.raises(ValidationError):
        _create(password=" abc123")


def test_phone_valid_and_invalid():
    """手机号必须 11 位、1 开头，合法时原样保留。"""
    assert _create(phone="13800138000").phone == "13800138000"
    for bad in ["1234", "23800138000", "1380013800a", "138001380001"]:
        with pytest.raises(ValidationError):
            _create(phone=bad)


def test_optional_fields_default_none():
    """选填字段不传时为 None，不影响创建。"""
    user = _create()
    assert user.phone is None
    assert user.nickname is None


def test_nickname_blank_rejected():
    """昵称传纯空白视为非法。"""
    with pytest.raises(ValidationError):
        _create(nickname="   ")


def test_user_update_phone_validation():
    """修改接口复用同一手机号校验。"""
    assert UserUpdate(nickname="新昵称").nickname == "新昵称"
    with pytest.raises(ValidationError):
        UserUpdate(phone="110")
