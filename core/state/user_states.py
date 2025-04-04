from abc import ABC, abstractmethod
from core.controller.logger import log


class UserState(ABC):
    @abstractmethod
    def change_user_state(self, user):
        pass
    
    @abstractmethod
    def __str__(self):
        pass
    
class AuthenticatedState(UserState):
    @log
    def change_user_state(self, user):
        user.state = NotAuthenticatedState()

    def __str__(self):
        return True

class NotAuthenticatedState(UserState):
    @log
    def change_user_state(self, user):
        user.state = AuthenticatedState()
    
    def __str__(self):
        return False