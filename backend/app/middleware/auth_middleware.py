from flask import request, jsonify
from app.services.jwt_service import JWTService

def token_required(f):
    """Декоратор для защиты маршрутов"""
    def decorated(*args, **kwargs):
        token = None
        
        # Получение токена из заголовка
        if 'Authorization' in request.headers:
            auth_header = request.headers['Authorization']
            if auth_header.startswith('Bearer '):
                token = auth_header.split(' ')[1]
        
        if not token:
            return jsonify({'error': 'Токен отсутствует'}), 401
        
        # Верификация токена
        payload = JWTService.verify_token(token)
        if not payload:
            return jsonify({'error': 'Невалидный токен'}), 401
        
        # Добавление информации о пользователе в запрос
        request.user = payload
        return f(*args, **kwargs)
    
    decorated.__name__ = f.__name__
    return decorated