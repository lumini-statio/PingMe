from core.state.user_states import UserState, NotAuthenticatedState, AuthenticatedState
from core.controller.utils.hasher import hash_password
from core.models.models import UserModel
from core.controller.utils.logger import log
import traceback


class User:
    '''The Python code defines a User class with methods for login, logout, and checking
    authentication status based on provided username and password.
    
    Parameters
    ----------
    username : str
        The `username` parameter is a string that represents the username entered by the user trying
    to log in. It is used to identify the user and validate their credentials during the login
    process.
    password : str
        The `password` parameter in the `login` method is a string that represents the password
    entered by the user during the login process. It is used to authenticate the user and grant
    access to the system if the password matches the one stored in the database for the
    corresponding username.
    '''
    def __init__(
            self,
            username: str=None,
            password: str=None,
            id: int=None
        ):
        self._id: int = id
        self._state = NotAuthenticatedState()
        self._username: str = username
        self._password: bytes = password
    '''
    --------------------------------------------------------------------------
    GETTERS & SETTERS
    --------------------------------------------------------------------------
    '''
    @property
    def id(self) -> int:
        return self._id

    @id.setter
    def id(self, id: int) -> None:
        self._id = id

    @property
    def state(self) -> UserState:
        return self._state

    @state.setter
    def state(self, state: UserState) -> None:
        self._state = state
    
    @property
    def username(self) -> str:
        return self._username
    
    @username.setter
    def username(self, username: str) -> None:
        self._username = username
    
    @property
    def password(self) -> bytes:
        return self._password

    @password.setter
    def password(self, password: str) -> None:
        self._password = password
    
    '''
    CLASS METHODS
    '''
    @log
    def login(self, username: str, password: str):
        '''This Python function is a login method that checks if the username and password are provided,
        hashes the password, retrieves users from a data access object, and attempts to find a user with
        matching credentials.
        
        Parameters
        ----------
        username : str
            The `username` parameter in the `login` method is a string that represents the username entered
        by the user trying to log in. It is used to identify the user and validate their credentials
        during the login process.
        password : str
            The `password` parameter in the `login` method is a string that represents the password entered
        by the user during the login process. It is used to authenticate the user and grant access to
        the system if the password matches the one stored in the database for the corresponding
        username.
        
        Returns
        -------
            The `login` method is returning a generator object `founded` that contains users whose username
        and hashed password match the input username and password.
        '''
        try:
            if not password and not username:
                raise ValueError('You must to complete Password and Username Fields')
            if not password:
                raise ValueError('Password field cannot be empty')
            if not username:
                raise ValueError('Username field cannot be empty')
            
            password_hashed = hash_password(password)
            users = UserModel.select().where(UserModel.username == username, UserModel.password == password_hashed)
            
            founded = [(um.id, um.username, um.password) for um in users]
            
            return founded
        except Exception:
            log(f'{__file__} - {traceback.format_exc()}')


    @log
    def is_authenticated(self):
        '''
        if the user is authenticated returns True,
        if not, returns False
        '''
        if isinstance(self.state, AuthenticatedState):
            return True
        elif isinstance(self.state, NotAuthenticatedState):
            return False
    
    def __str__(self):
        return self.username

