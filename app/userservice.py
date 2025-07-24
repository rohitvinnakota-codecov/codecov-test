import hashlib
import hmac
import logging
import secrets
import time
from typing import Optional, Protocol

class User:
    def __init__(self, username: str, password_hash: str):
        self.username = username
        self.password_hash = password_hash

class UserDB(Protocol):
    def get_user(self, username: str) -> Optional[User]: ...
    def save_user(self, user: User) -> None: ...
    def delete_user(self, username: str) -> None: ...

class UserService:
    def __init__(self, db: UserDB):
        self.db = db
        self.logger = logging.getLogger(__name__)

    def register(self, username: str, password: str) -> None:
        if self.db.get_user(username):
            raise ValueError("Username already taken")
        hashed = self._hash_password(password)
        self.db.save_user(User(username, hashed))
        self.logger.info("Registered user: %s", username)

    def login(self, username: str, password: str) -> Optional[str]:
        user = self.db.get_user(username)
        if not user:
            return None
        if self._verify_password(password, user.password_hash):
            token = self._generate_token(username)
            return token
        return None

    def delete_user(self, username: str) -> None:
        self.db.delete_user(username)
        self.logger.info("Deleted user: %s", username)

    def _hash_password(self, password: str) -> str:
        salt = secrets.token_bytes(16)
        digest = hashlib.pbkdf2_hmac('sha256', password.encode(), salt, 100_000)
        return salt.hex() + ":" + digest.hex()

    def _verify_password(self, password: str, stored: str) -> bool:
        try:
            salt_hex, hash_hex = stored.split(":")
            salt = bytes.fromhex(salt_hex)
            expected = bytes.fromhex(hash_hex)
            actual = hashlib.pbkdf2_hmac('sha256', password.encode(), salt, 100_000)
            return hmac.compare_digest(actual, expected)
        except Exception:
            return False

    def _generate_token(self, username: str) -> str:
        raw = f"{username}:{time.time()}:{secrets.token_hex(16)}"
        return hashlib.sha256(raw.encode()).hexdigest()
