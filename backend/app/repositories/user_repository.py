import json
import os
from datetime import datetime
from app.models import User
import logging

logger = logging.getLogger(__name__)

USERS_FILE = 'data/users.json'

class UserRepository:
    
    @staticmethod
    def _ensure_data_file():
        """Создает файл пользователей если его нет"""
        if not os.path.exists(USERS_FILE):
            os.makedirs(os.path.dirname(USERS_FILE), exist_ok=True)
            with open(USERS_FILE, 'w', encoding='utf-8') as f:
                json.dump([], f, indent=2)
    
    @staticmethod
    def get_all():
        """Получить всех пользователей"""
        UserRepository._ensure_data_file()
        
        try:
            with open(USERS_FILE, 'r', encoding='utf-8') as f:
                data = json.load(f)
                users = []
                for item in data:
                    user = User(
                        id=item['id'],
                        username=item['username'],
                        email=item['email'],
                        password_hash=item['password_hash'],
                        created_at=item['created_at']
                    )
                    users.append(user)
                return users
        except Exception as e:
            logger.error(f'Error loading users: {str(e)}')
            return []
    
    @staticmethod
    def get_by_username(username: str):
        """Найти пользователя по имени"""
        users = UserRepository.get_all()
        for user in users:
            if user.username == username:
                return user
        return None
    
    @staticmethod
    def get_by_email(email: str):
        """Найти пользователя по email"""
        users = UserRepository.get_all()
        for user in users:
            if user.email == email:
                return user
        return None
    
    @staticmethod
    def create(username: str, email: str, password: str):
        """Создать нового пользователя"""
        users = UserRepository.get_all()
        
        # Проверка на существующего пользователя
        if UserRepository.get_by_username(username):
            raise ValueError('Пользователь с таким именем уже существует')
        
        if UserRepository.get_by_email(email):
            raise ValueError('Пользователь с таким email уже существует')
        
        # Генерация ID
        new_id = max([u.id for u in users], default=0) + 1
        
        # Создание пользователя
        user = User(
            id=new_id,
            username=username,
            email=email,
            password_hash=User.hash_password(password),
            created_at=datetime.now().isoformat()
        )
        
        # Сохранение
        users.append(user)
        UserRepository._save_users(users)
        
        return user
    
    @staticmethod
    def _save_users(users):
        """Сохранить пользователей в файл"""
        try:
            with open(USERS_FILE, 'w', encoding='utf-8') as f:
                json.dump([{
                    'id': u.id,
                    'username': u.username,
                    'email': u.email,
                    'password_hash': u.password_hash,
                    'created_at': u.created_at
                } for u in users], f, indent=2, ensure_ascii=False)
            return True
        except Exception as e:
            logger.error(f'Error saving users: {str(e)}')
            return False
    
    @staticmethod
    def authenticate(username: str, password: str):
        """Аутентификация пользователя"""
        user = UserRepository.get_by_username(username)
        if user and user.check_password(password):
            return user
        return None