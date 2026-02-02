from core.db import execute_query
from django.contrib.auth.hashers import make_password, check_password

class User:
    """
    Model representing a user in the system.
    """
    @staticmethod
    def create(username, email, password, role='user'):
        """
        Create a new user in the database.
        """
        hashed_password = make_password(password)
        query = """
            INSERT INTO app_users (username, email, password, role)
            VALUES (%s, %s, %s, %s)
            RETURNING id, username, email, role, created_at;
        """
        return execute_query(query, (username, email, hashed_password, role), fetch_one=True)

    @staticmethod
    def get_by_username(username):
        """
        Retrieve a user by their username.
        """
        query = "SELECT * FROM app_users WHERE username = %s;"
        return execute_query(query, (username,), fetch_one=True)

    @staticmethod
    def get_by_email(email):
        """
        Retrieve a user by their email address.
        """
        query = "SELECT * FROM app_users WHERE email = %s;"
        return execute_query(query, (email,), fetch_one=True)

    @staticmethod
    def get_by_username_or_email(identifier):
        """
        Retrieve a user by either username or email.
        """
        query = "SELECT * FROM app_users WHERE username = %s OR email = %s;"
        return execute_query(query, (identifier, identifier), fetch_one=True)

    @staticmethod
    def get_by_id(user_id):
        """
        Retrieve a user by their ID.
        """
        query = "SELECT * FROM app_users WHERE id = %s;"
        return execute_query(query, (user_id,), fetch_one=True)

    @staticmethod
    def check_password(plain_password, hashed_password):
        """
        Verify a password against its hash.
        """
        return check_password(plain_password, hashed_password)
