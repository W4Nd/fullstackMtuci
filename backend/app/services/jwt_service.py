import jwt
import datetime
from flask import current_app
import os
import logging

logger = logging.getLogger(__name__)

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
        
        secret_key = os.environ.get('SECRET_KEY', 'fallback-secret-key-change-in-production')
        print(f"🔐 Creating token with SECRET_KEY: {secret_key[:20]}..." if secret_key else "⚠️ SECRET_KEY is empty!")
        token = jwt.encode(payload, secret_key, algorithm='HS256')
        print(f"✅ Token created: {token[:30]}...")
        return token
    
    @staticmethod
    def verify_token(token: str):
        """Верификация JWT токена"""
        try:
            secret_key = os.environ.get('SECRET_KEY', 'fallback-secret-key-change-in-production')
            print(f"🔐 Verifying token with SECRET_KEY: {secret_key[:20]}..." if secret_key else "⚠️ SECRET_KEY is empty!")
            payload = jwt.decode(token, secret_key, algorithms=['HS256'])
            print(f"✅ Token verified successfully: {payload}")
            return payload
        except jwt.ExpiredSignatureError:
            print(f"❌ Token expired")
            return None
        except jwt.InvalidTokenError as e:
            print(f"❌ Invalid token: {e}")
            return None
