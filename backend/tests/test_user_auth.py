import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent.parent.parent))

from backend.app.core.auth import create_access_token, verify_access_token


def test_jwt_token_create_and_verify():
    test_openid = "o123456789abcdef"
    token = create_access_token(data={"sub": test_openid})
    payload = verify_access_token(token)
    assert payload is not None
    assert payload["sub"] == test_openid


def test_jwt_invalid_token():
    bad_token = "abcdef.fake.token"
    payload = verify_access_token(bad_token)
    assert payload is None
