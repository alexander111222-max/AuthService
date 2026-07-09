import pytest
from src.utils.auth import JWTManager, PasswordManager
from src.utils.exceptions import TokenExpiredError, InvalidTokenError


jwt_manager = JWTManager(secret="test_secret")
password_manager = PasswordManager()


def test_hash_password():
    hashed = password_manager.hash_password("mypassword")
    assert hashed != "mypassword"
    assert len(hashed) > 0


def test_verify_password_correct():
    hashed = password_manager.hash_password("mypassword")
    assert password_manager.verify_password("mypassword", hashed) is True


def test_verify_password_wrong():
    hashed = password_manager.hash_password("mypassword")
    assert password_manager.verify_password("wrongpassword", hashed) is False


def test_verify_password_empty():
    assert password_manager.verify_password("", "somehash") is False


def test_create_token():
    token = jwt_manager.create_token({"user_id": 1, "role": "user"})
    assert isinstance(token, str)
    assert len(token.split(".")) == 3


def test_decode_token():
    payload = {"user_id": 1, "role": "admin"}
    token = jwt_manager.create_token(payload)
    decoded = jwt_manager.decode_token(token)
    assert decoded["user_id"] == 1
    assert decoded["role"] == "admin"


def test_decode_token_invalid():
    with pytest.raises(InvalidTokenError):
        jwt_manager.decode_token("invalid.token.here")


def test_decode_token_tampered():
    import base64, json
    token = jwt_manager.create_token({"user_id": 1, "role": "user"})
    header, payload, signature = token.split(".")

    # меняем user_id в payload
    fake_payload = base64.urlsafe_b64encode(
        json.dumps({"user_id": 999, "role": "admin"}).encode()
    ).decode().rstrip("=")

    tampered_token = f"{header}.{fake_payload}.{signature}"
    with pytest.raises(InvalidTokenError):
        jwt_manager.decode_token(tampered_token)


def test_token_expired():
    token = jwt_manager.create_token({"user_id": 1}, ttl=-1)
    with pytest.raises(TokenExpiredError):
        jwt_manager.decode_token(token)


def test_validate_token_valid():
    token = jwt_manager.create_token({"user_id": 1})
    assert jwt_manager.validate_token(token) is True


def test_validate_token_invalid():
    assert jwt_manager.validate_token("not.a.token") is False