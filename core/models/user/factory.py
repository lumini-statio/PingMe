from core.models.user.entity import User
from core.models.models import UserModel
from core.controller.utils.hasher import hash_password
from core.controller.utils.logger import log


class UserFactory():
    """
    Users creation class
    """
    @classmethod
    def create(cls, username: str, value: str) -> bool:
        """
        Insert the user in database with hashed password. 
        If the user already exists, returns True, 
        if not, returns False
        """
        username = username.strip()
        password = hash_password(value)

        exists = UserModel.select().where(UserModel.username == username).exists()

        if exists:
            return {
                'user_exists': True,
                'user': None
            }
        
        user_to_db = UserModel(
            username=username.strip(),
            password=password
        )

        user_to_db.save()

        my_user = User(
            id=user_to_db.id,
            username=username.strip(), 
            password=password
        )

        return {
            'user_exists': exists,
            'user': my_user.__str__()
        }
            