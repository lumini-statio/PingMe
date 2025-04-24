from core.models.user.entity import User
from core.models.models import UserModel, session
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

        exists = session.query(UserModel)\
                .filter_by(
                    username = username
                ).first()
        
        if exists is not None:
            return {
                'user_exists': True,
                'user': None
            }
        
        user_to_db = UserModel(
            username=username.strip(),
            password=password
        )

        session.add(user_to_db)
        session.commit()

        my_user = User(
            id=user_to_db.id,
            username=username.strip(), 
            password=password
        )

        return {
            'user_exists': False,
            'user': str(my_user)
        }
            