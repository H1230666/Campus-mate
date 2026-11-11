from core.auth import create_access_token, verify_access_token

def test_jwt_token_create_and_verify():
    test_openid = "o123456789abcdef"
    token = create_access_token(test_openid)
    res_openid = verify_access_token(token)
    assert res_openid == test_openid

def test_jwt_invalid_token():
    bad_token = "abcdef.fake.token"
    res = verify_access_token(bad_token)
    assert res is None
