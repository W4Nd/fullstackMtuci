from flask import Blueprint, request, jsonify
from app.repositories.user_repository import UserRepository
from app.services.jwt_service import JWTService
import logging

logger = logging.getLogger(__name__)

bp = Blueprint('auth', __name__)

@bp.route('/auth/register', methods=['POST'])
def register():
    """Регистрация нового пользователя"""
    try:
        data = request.json
        
        # Валидация
        if not data.get('username') or not data.get('email') or not data.get('password'):
            return jsonify({'error': 'Все поля обязательны'}), 400
        
        if len(data['password']) < 6:
            return jsonify({'error': 'Пароль должен быть не менее 6 символов'}), 400
        
        # Создание пользователя
        user = UserRepository.create(
            username=data['username'],
            email=data['email'],
            password=data['password']
        )
        
        # Создание токена
        token = JWTService.create_token(user.id, user.username)
        
        return jsonify({
            'message': 'Пользователь успешно зарегистрирован',
            'user': user.to_dict(),
            'token': token
        }), 201
        
    except ValueError as e:
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        logger.error(f'Error in register: {str(e)}')
        return jsonify({'error': 'Внутренняя ошибка сервера'}), 500

@bp.route('/auth/login', methods=['POST'])
def login():
    """Аутентификация пользователя"""
    try:
        data = request.json
        
        if not data.get('username') or not data.get('password'):
            return jsonify({'error': 'Имя пользователя и пароль обязательны'}), 400
        
        # Аутентификация
        user = UserRepository.authenticate(data['username'], data['password'])
        if not user:
            return jsonify({'error': 'Неверное имя пользователя или пароль'}), 401
        
        # Создание токена
        token = JWTService.create_token(user.id, user.username)
        
        return jsonify({
            'message': 'Вход выполнен успешно',
            'user': user.to_dict(),
            'token': token
        }), 200
        
    except Exception as e:
        logger.error(f'Error in login: {str(e)}')
        return jsonify({'error': 'Внутренняя ошибка сервера'}), 500

@bp.route('/auth/verify', methods=['POST'])
def verify_token():
    """Проверка валидности токена"""
    try:
        token = request.json.get('token')
        if not token:
            return jsonify({'error': 'Токен обязателен'}), 400
        
        payload = JWTService.verify_token(token)
        if not payload:
            return jsonify({'error': 'Невалидный токен'}), 401
        
        return jsonify({
            'valid': True,
            'user': {
                'user_id': payload['user_id'],
                'username': payload['username']
            }
        }), 200
        
    except Exception as e:
        logger.error(f'Error verifying token: {str(e)}')
        return jsonify({'error': 'Внутренняя ошибка сервера'}), 500