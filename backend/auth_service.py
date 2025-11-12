"""
Authentication Service
Handles user authentication with JWT tokens and password hashing
"""
import os
import jwt
import bcrypt
from datetime import datetime, timedelta, timezone
from typing import Optional, Dict, Any
import logging

logger = logging.getLogger(__name__)

class AuthService:
    """Service for user authentication"""
    
    def __init__(self):
        self.jwt_secret = os.environ.get('JWT_SECRET', 'your-secret-key-change-in-production')
        self.jwt_algorithm = 'HS256'
        self.token_expiry_hours = 24 * 7  # 7 days
        
    def hash_password(self, password: str) -> str:
        """Hash a password using bcrypt"""
        salt = bcrypt.gensalt()
        hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
        return hashed.decode('utf-8')
    
    def verify_password(self, password: str, hashed_password: str) -> bool:
        """Verify a password against its hash"""
        try:
            return bcrypt.checkpw(
                password.encode('utf-8'),
                hashed_password.encode('utf-8')
            )
        except Exception as e:
            logger.error(f"Password verification error: {str(e)}")
            return False
    
    def create_token(self, user_data: Dict[str, Any]) -> str:
        """Create a JWT token for a user"""
        payload = {
            'user_id': user_data['id'],
            'email': user_data['email'],
            'name': user_data['name'],
            'plan': user_data['plan'],
            'state': user_data.get('state', ''),
            'exp': datetime.now(timezone.utc) + timedelta(hours=self.token_expiry_hours),
            'iat': datetime.now(timezone.utc)
        }
        
        token = jwt.encode(payload, self.jwt_secret, algorithm=self.jwt_algorithm)
        return token
    
    def verify_token(self, token: str) -> Optional[Dict[str, Any]]:
        """Verify and decode a JWT token"""
        try:
            payload = jwt.decode(token, self.jwt_secret, algorithms=[self.jwt_algorithm])
            return payload
        except jwt.ExpiredSignatureError:
            logger.warning("Token has expired")
            return None
        except jwt.InvalidTokenError as e:
            logger.warning(f"Invalid token: {str(e)}")
            return None
    
    def authenticate_user(self, email: str, password: str, db) -> Optional[Dict[str, Any]]:
        """
        Authenticate a user with email and password
        Returns user data if successful, None otherwise
        """
        # Check admin credentials from environment
        admin_email = os.environ.get('ADMIN_EMAIL')
        admin_password_hash = os.environ.get('ADMIN_PASSWORD_HASH')
        admin_name = os.environ.get('ADMIN_NAME', 'Admin')
        admin_state = os.environ.get('ADMIN_STATE', 'NV')
        
        if email == admin_email:
            if self.verify_password(password, admin_password_hash):
                return {
                    'id': 'admin-user',
                    'email': admin_email,
                    'name': admin_name,
                    'plan': 'Enterprise',
                    'state': admin_state,
                    'mls_access': True
                }
        
        # Future: Check database for other users
        # user = await db.users.find_one({"email": email})
        
        return None
    
    def has_mls_access(self, user: Dict[str, Any], state: str = None) -> bool:
        """
        Check if user has MLS access for their state
        Enterprise users with matching state or admin have access
        """
        if not user:
            return False
        
        # Must be Enterprise plan
        if user.get('plan') != 'Enterprise':
            return False
        
        # Admin always has access
        if user.get('id') == 'admin-user':
            return True
        
        # Check state match if specified
        if state:
            return user.get('state', '').upper() == state.upper()
        
        # Has MLS access flag
        return user.get('mls_access', False)
