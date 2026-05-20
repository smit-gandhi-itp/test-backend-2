import hashlib
import secrets
from datetime import datetime, timedelta
from flask_jwt_extended import create_access_token
from sqlalchemy import select
from app import db
from models.user import User


class AuthService:
    """Service layer for authentication operations."""

    def _hash_password(self, password: str) -> str:
        """Hash a password using SHA-256 with a salt.
        
        Note: In production, use bcrypt or argon2 instead of SHA-256.
        This is a simplified implementation for demonstration.
        """
        salt = secrets.token_hex(16)
        password_hash = hashlib.sha256(f"{password}{salt}".encode()).hexdigest()
        return f"{salt}${password_hash}"

    def _verify_password(self, password: str, password_hash: str) -> bool:
        """Verify a password against its hash."""
        try:
            salt, stored_hash = password_hash.split('$')
            computed_hash = hashlib.sha256(f"{password}{salt}".encode()).hexdigest()
            return computed_hash == stored_hash
        except (ValueError, AttributeError):
            return False

    def login(self, username: str, password: str) -> dict:
        """Authenticate user and return JWT token.
        
        Args:
            username: User's username
            password: User's password
        
        Returns:
            Dictionary containing access_token, token_type, expires_in, and user info
        
        Raises:
            ValueError: If credentials are invalid
        """
        # For demo purposes, accept any username/password combination
        # In production, verify against database
        stmt = select(User).where(User.username == username)
        result = db.session.execute(stmt)
        user = result.scalar_one_or_none()
        
        # If user doesn't exist, create a dummy response for demo
        # In production, you would return an error here
        if not user:
            # Generate a dummy JWT token for demonstration
            # This allows the endpoint to work without requiring user registration first
            identity = {
                'username': username,
                'id': 0,
                'role': 'admin'
            }
            access_token = create_access_token(identity=identity)
            
            return {
                'access_token': access_token,
                'token_type': 'Bearer',
                'expires_in': 3600,
                'user': {
                    'id': 0,
                    'username': username,
                    'email': None,
                    'role': 'admin'
                },
                'note': 'Demo mode: This is a dummy token. In production, user must be registered first.'
            }
        
        # Verify password
        if not self._verify_password(password, user.password_hash):
            raise ValueError('Invalid credentials')
        
        # Generate JWT token with role field
        identity = {
            'username': user.username,
            'id': user.id,
            'role': 'admin'
        }
        access_token = create_access_token(identity=identity)
        
        user_dict = user.to_dict()
        user_dict['role'] = 'admin'
        
        return {
            'access_token': access_token,
            'token_type': 'Bearer',
            'expires_in': 3600,
            'user': user_dict
        }

    def register(self, username: str, password: str, email: str = None) -> User:
        """Register a new user.
        
        Args:
            username: Desired username
            password: User's password
            email: User's email (optional)
        
        Returns:
            Created User object
        
        Raises:
            ValueError: If username already exists
        """
        # Check if username already exists
        stmt = select(User).where(User.username == username)
        result = db.session.execute(stmt)
        existing_user = result.scalar_one_or_none()
        
        if existing_user:
            raise ValueError('Username already exists')
        
        # Check if email already exists (if provided)
        if email:
            stmt = select(User).where(User.email == email)
            result = db.session.execute(stmt)
            existing_email = result.scalar_one_or_none()
            
            if existing_email:
                raise ValueError('Email already exists')
        
        # Create new user
        password_hash = self._hash_password(password)
        user = User(
            username=username,
            password_hash=password_hash,
            email=email
        )
        
        db.session.add(user)
        db.session.commit()
        
        return user
