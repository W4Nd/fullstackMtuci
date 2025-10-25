import jwt
import datetime
from flask import current_app
import os

class JWTService:
    """Сервис для работы с JWT токенами"""
    
    @staticmethod
    def create_token(user_id: int, username: str):
        """Создание JWT токена"""
        payload = {
            'user_id': user_id,
            'username': username,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(days=7),
            'iat': datetime.datetime.utcnow()
        }
        
        secret_key = os.environ.get('JWT_SECRET_KEY', 'fallback-secret-key-change-in-production')
        return jwt.encode(payload, secret_key, algorithm='HS256')
    
    @staticmethod
    def verify_token(token: str):
        """Верификация JWT токена"""
        try:
            secret_key = os.environ.get('JWT_SECRET_KEY', 'fallback-secret-key-change-in-production')
            payload = jwt.decode(token, secret_key, algorithms=['HS256'])
            return payload
        except jwt.ExpiredSignatureError:
            return None
        except jwt.InvalidTokenError:
            return None