from core.models.user.user import User
from core.models.models import UserModel
from core.models.user.hasher import hash_password
from core.controller.logger import log


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
        password = hash_password(value)

        user = User(
            username=username.strip(), 
            password=password
        )

        users = UserModel.select()

        exists = False

        for element in users:
            if element[1] == user.username:
                exists = True
                break

        if exists == False:
            my_user = UserModel(
                username = user.username,
                password = user.password
            )

            my_user.save()

            users = UserModel.select()

            final_user = [user for user in users if user[1]==username and user[2]==password]

            if final_user != None:
                user.set_id(final_user[0][0])

                return {
                    'user_exists': exists,
                    'user': user
                }
            else:
                log(f'{__file__} - final_user its void')

        
        return {
            'user_exists': exists,
            'user': None
        }
        
            