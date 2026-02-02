from .models import User
from authentication.utils import generate_token
from core.api_utils import ValidationError, UnauthorizedError

class AuthService:
    """
    Service class for handling authentication-related logic.
    """
    @staticmethod
    def register_user(username, email, password):
        """
        Register a new user.
        """
        if User.get_by_username(username):
            raise ValidationError('Username already exists')

        if User.get_by_email(email):
            raise ValidationError('Email already exists')
            
        user = User.create(username, email, password, role='user')
        
        return user

    @staticmethod
    def login_user(username, password):
        """
        Params:
            username (str): The username or email of the user.
            password (str): The user's password.
        
        Returns:
            tuple: A tuple containing the user object and the generated token.
        
        Raises:
            UnauthorizedError: If the credentials are invalid.
        """
        user = User.get_by_username_or_email(username)
        if not user or not User.check_password(password, user['password']):
            raise UnauthorizedError('Invalid credentials')
            
        token = generate_token(user['id'], user['role'])
        return user, token
