from flask import request, jsonify, g
from app.services.jwt_service import JWTService
import logging


logger = logging.getLogger(__name__)


def token_required(f):
    """Декоратор для защиты маршрутов"""
    from functools import wraps

    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        
        print(f"\n🔍 Checking authorization...")
        
        if 'Authorization' in request.headers:
            auth_header = request.headers['Authorization']
            print(f"✅ Authorization header found: {auth_header[:30]}...")
            if auth_header.startswith('Bearer '):
                token = auth_header.split(' ')[1]
                print(f"✅ Token extracted: {token[:30]}...")
        
        if not token:
            print(f"❌ No token found!")
            return jsonify({'error': 'Токен отсутствует'}), 401
        
        print(f"🔐 Verifying token...")
        print(f"🔐 Token to verify: {token}")
        payload = JWTService.verify_token(token)
        print(f"🔐 Payload after verify: {payload}")
        
        if not payload:
            print(f"❌ Token verification failed! Payload is None/False")
            return jsonify({'error': 'Невалидный токен'}), 401
        
        print(f"✅ Token verified! User: {payload.get('username')}, ID: {payload.get('user_id')}")
        
        g.user_id = payload['user_id']
        g.username = payload['username']
        request.user = payload  
        
        print(f"✅ User context set: g.user_id={g.user_id}, g.username={g.username}")
        
        return f(*args, **kwargs)
    
    return decorated


def get_current_user_id():
    """Получить ID текущего пользователя из контекста"""
    return getattr(g, 'user_id', None)


def get_current_username():
    """Получить username текущего пользователя из контекста"""
    return getattr(g, 'username', None)
