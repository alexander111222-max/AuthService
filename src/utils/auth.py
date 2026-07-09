import hashlib
import hmac
import json
import time
import bcrypt
from typing import Dict, Any, Optional
from jose.utils import base64url_encode, base64url_decode

from src.config import settings
from src.utils.exceptions import TokenExpiredError, InvalidTokenError


class JWTManager:

    def __init__(self, secret: str, default_ttl: int = 3600):
        self.secret = secret.encode('utf-8')
        self.algorithm = settings.ALGORITHM
        self.default_ttl = default_ttl
        self.header = {"typ": "JWT", "alg": self.algorithm}

    @staticmethod
    def _encode_part(data: Dict[str, Any]) -> str:
        json_data = json.dumps(data, separators=(',', ':')).encode('utf-8')
        return base64url_encode(json_data).decode('utf-8')

    @staticmethod
    def _decode_part(encoded_data: str) -> Dict[str, Any]:
        decoded_bytes = base64url_decode(encoded_data.encode('utf-8'))
        return json.loads(decoded_bytes.decode('utf-8'))

    def _create_signature(self, message: str) -> str:
        signature = hmac.new(
            self.secret,
            message.encode('utf-8'),
            hashlib.sha256
        ).digest()
        return base64url_encode(signature).decode('utf-8')

    def create_token(self, payload: Dict[str, Any], ttl: Optional[int] = None) -> str:
        payload = payload.copy()
        payload['iat'] = int(time.time())
        payload['exp'] = int(time.time()) + (ttl or self.default_ttl)

        header_encoded = self._encode_part(self.header)
        payload_encoded = self._encode_part(payload)
        message = f"{header_encoded}.{payload_encoded}"
        signature = self._create_signature(message)
        return f"{message}.{signature}"

    def validate_token(self, token: str) -> bool:
        try:
            parts = token.split(".")
            if len(parts) != 3:
                return False

            header_encoded, payload_encoded, signature_provided = parts
            message = f"{header_encoded}.{payload_encoded}"
            signature_expected = self._create_signature(message)

            return hmac.compare_digest(signature_expected, signature_provided)
        except Exception:
            return False

    def decode_token(self, token: str) -> Dict[str, Any]:
        if not self.validate_token(token):
            raise InvalidTokenError("Невалидная сигнатура токена")

        try:
            payload_encoded = token.split(".")[1]
            payload = self._decode_part(payload_encoded)
        except (IndexError, json.JSONDecodeError) as e:
            raise InvalidTokenError(f"Невалидный формат токена: {e}")

        if 'exp' in payload and payload['exp'] < int(time.time()):
            raise TokenExpiredError("Токен протух")

        return payload


class PasswordManager:

    def __init__(self):
        self.default_rounds = 12

    def hash_password(self, password: str, rounds: Optional[int] = None) -> str:
        if not password:
            raise ValueError("Пароль не может быть пустым")

        password_bytes = password.encode("utf-8")
        salt = bcrypt.gensalt(rounds=rounds or self.default_rounds)
        hashed_password = bcrypt.hashpw(password_bytes, salt)
        return hashed_password.decode("utf-8")

    @staticmethod
    def verify_password(password: str, hashed_password: str) -> bool:
        if not password or not hashed_password:
            return False

        try:
            password_bytes = password.encode("utf-8")
            hashed_bytes = hashed_password.encode("utf-8")
            return bcrypt.checkpw(password_bytes, hashed_bytes)
        except Exception:
            return False
