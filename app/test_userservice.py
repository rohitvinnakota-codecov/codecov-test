import hashlib
import hmac
import logging
import re
import time
from typing import Dict, Optional
from unittest.mock import Mock, patch

from .userservice import User, UserService


class MockUserDB:
    """Mock implementation of UserDB for testing"""
    def __init__(self):
        self.users: Dict[str, User] = {}

    def get_user(self, username: str) -> Optional[User]:
        return self.users.get(username)

    def save_user(self, user: User) -> None:
        self.users[user.username] = user

    def delete_user(self, username: str) -> None:
        if username in self.users:
            del self.users[username]


def test_user_creation():
    """Test User class instantiation and attributes"""
    user = User("testuser", "testhash")
    assert user.username == "testuser"
    assert user.password_hash == "testhash"


def test_userservice_init():
    """Test UserService initialization"""
    mock_db = MockUserDB()
    service = UserService(mock_db)
    assert service.db == mock_db
    assert service.logger.name == "app.userservice"


def test_register_success():
    """Test successful user registration"""
    mock_db = MockUserDB()
    service = UserService(mock_db)
    
    with patch.object(service.logger, 'info') as mock_log:
        service.register("newuser", "password123")
        
    # Verify user was saved
    saved_user = mock_db.get_user("newuser")
    assert saved_user is not None
    assert saved_user.username == "newuser"
    
    # Verify password was hashed (should contain salt:hash format)
    assert ":" in saved_user.password_hash
    salt_hex, hash_hex = saved_user.password_hash.split(":")
    assert len(salt_hex) == 32  # 16 bytes = 32 hex chars
    assert len(hash_hex) == 64  # 32 bytes = 64 hex chars
    
    # Verify logging
    mock_log.assert_called_once_with("Registered user: %s", "newuser")


def test_register_existing_user():
    """Test registration with existing username"""
    mock_db = MockUserDB()
    service = UserService(mock_db)
    
    # Register first user
    service.register("existinguser", "password123")
    
    # Try to register same username again
    try:
        service.register("existinguser", "password456")
        assert False, "Expected ValueError"
    except ValueError as e:
        assert str(e) == "Username already taken"


def test_login_success():
    """Test successful login"""
    mock_db = MockUserDB()
    service = UserService(mock_db)
    
    # Register a user first
    service.register("loginuser", "mypassword")
    
    # Login with correct credentials
    token = service.login("loginuser", "mypassword")
    
    assert token is not None
    assert isinstance(token, str)
    assert len(token) == 64  # SHA256 hash is 64 hex chars


def test_login_wrong_password():
    """Test login with incorrect password"""
    mock_db = MockUserDB()
    service = UserService(mock_db)
    
    # Register a user first
    service.register("loginuser", "mypassword")
    
    # Login with wrong password
    token = service.login("loginuser", "wrongpassword")
    
    assert token is None


def test_login_nonexistent_user():
    """Test login with non-existent username"""
    mock_db = MockUserDB()
    service = UserService(mock_db)
    
    # Try to login without registering
    token = service.login("nonexistent", "anypassword")
    
    assert token is None


def test_delete_user():
    """Test user deletion"""
    mock_db = MockUserDB()
    service = UserService(mock_db)
    
    # Register a user first
    service.register("deleteuser", "password123")
    assert mock_db.get_user("deleteuser") is not None
    
    # Delete the user
    with patch.object(service.logger, 'info') as mock_log:
        service.delete_user("deleteuser")
    
    # Verify user was deleted
    assert mock_db.get_user("deleteuser") is None
    
    # Verify logging
    mock_log.assert_called_once_with("Deleted user: %s", "deleteuser")


def test_hash_password():
    """Test password hashing functionality"""
    mock_db = MockUserDB()
    service = UserService(mock_db)
    
    hashed1 = service._hash_password("testpassword")
    hashed2 = service._hash_password("testpassword")
    
    # Same password should produce different hashes due to random salt
    assert hashed1 != hashed2
    
    # Both should be in salt:hash format
    assert ":" in hashed1
    assert ":" in hashed2
    
    # Verify format
    salt_hex1, hash_hex1 = hashed1.split(":")
    salt_hex2, hash_hex2 = hashed2.split(":")
    assert len(salt_hex1) == 32
    assert len(hash_hex1) == 64
    assert len(salt_hex2) == 32
    assert len(hash_hex2) == 64


def test_verify_password():
    """Test password verification"""
    mock_db = MockUserDB()
    service = UserService(mock_db)
    
    password = "testpassword"
    hashed = service._hash_password(password)
    
    # Correct password should verify
    assert service._verify_password(password, hashed) is True
    
    # Wrong password should not verify
    assert service._verify_password("wrongpassword", hashed) is False


def test_verify_password_invalid_format():
    """Test password verification with invalid stored hash format"""
    mock_db = MockUserDB()
    service = UserService(mock_db)
    
    # Test with invalid format (no colon)
    assert service._verify_password("password", "invalidhash") is False
    
    # Test with invalid hex
    assert service._verify_password("password", "invalid:hex") is False


def test_generate_token():
    """Test token generation"""
    mock_db = MockUserDB()
    service = UserService(mock_db)
    
    token1 = service._generate_token("user1")
    token2 = service._generate_token("user1")
    
    # Tokens should be different due to timestamp and random component
    assert token1 != token2
    
    # Tokens should be 64 character hex strings (SHA256)
    assert len(token1) == 64
    assert len(token2) == 64
    assert re.match(r'^[a-f0-9]{64}$', token1)
    assert re.match(r'^[a-f0-9]{64}$', token2)