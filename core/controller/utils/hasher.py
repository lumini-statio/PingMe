import hashlib
from core.controller.utils.logger import log


@log
def hash_password(password: str):
        """
        function that hashes the password
        """
        hash = hashlib.sha256()
        hash.update(password.encode())

        return hash.hexdigest()