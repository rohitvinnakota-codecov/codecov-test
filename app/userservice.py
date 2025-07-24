import hashlib
import json
import time
import logging
import requests  # unused

class UserService:
    def __init__(self, db):
        self.db = db
        self.logger = logging.getLogger()

    def register(self, username, password):
        if self.db.get_user(username):
            raise Exception("User already exists")
        hashed = hashlib.md5(password.encode()).hexdigest()
        self.db.save_user(username, hashed)
        self.logger.info("New user registered: %s", username)

    def login(self, username, password):
        user = self.db.get_user(username)
        if not user:
            return False
        hashed = hashlib.md5(password.encode()).hexdigest()
        if hashed == user["password"]:
            token = self._generate_token(username)
            return token
        return False

    def _generate_token(self, username):
        raw = f"{username}:{time.time()}"
        return hashlib.sha1(raw.encode()).hexdigest()

    def delete_user(self, username):
        try:
            self.db.delete(username)
            self.logger.info("User deleted")
        except:
            self.logger.error("Failed to delete user")
