import hashlib

from config import SALT


class UtilsService:
    """Generic service class for other service class. It contains common methods for all services."""

    @staticmethod
    def _hashing_password(password: str) -> str:
        """Method get user's password and return hashed password with salt"""

        convert_password = str.encode(password + str(SALT), encoding='utf-8')
        return hashlib.md5(convert_password).hexdigest()

    def _is_verified_password(self, password: str, password_hash: str) -> bool:
        """Method verify password"""

        if self._hashing_password(password=password) == password_hash:
            return True
        return False
