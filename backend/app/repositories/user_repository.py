from app.models import User
from app.database import db
import logging

logger = logging.getLogger(__name__)

class UserRepository:
    
    def __init__(self, db):  
        self.db = db
    
    @staticmethod
    def get_all():
        """Получить всех пользователей"""
        try:
            result = db.execute_query("SELECT * FROM users")
            return [User.from_db(row) for row in result]
        except Exception as e:
            logger.error(f'Error loading users: {str(e)}')
            return []
    
    @staticmethod
    def get_by_id(user_id: int):
        """Найти пользователя по ID"""
        try:
            result = db.execute_query("SELECT * FROM users WHERE id = %s", (user_id,))
            if result:
                return User.from_db(result[0])
            return None
        except Exception as e:
            logger.error(f'Error getting user by id: {str(e)}')
            return None
    
    @staticmethod
    def get_by_username(username: str):
        """Найти пользователя по имени"""
        try:
            result = db.execute_query("SELECT * FROM users WHERE username = %s", (username,))
            if result:
                return User.from_db(result[0])
            return None
        except Exception as e:
            logger.error(f'Error getting user by username: {str(e)}')
            return None
    
    @staticmethod
    def get_by_email(email: str):
        """Найти пользователя по email"""
        try:
            result = db.execute_query("SELECT * FROM users WHERE email = %s", (email,))
            if result:
                return User.from_db(result[0])
            return None
        except Exception as e:
            logger.error(f'Error getting user by email: {str(e)}')
            return None
    
    @staticmethod
    def create(username: str, email: str, password: str):
        """Создать нового пользователя"""
        try:
            # Проверка на существующего пользователя
            if UserRepository.get_by_username(username):
                raise ValueError('Пользователь с таким именем уже существует')
            
            if UserRepository.get_by_email(email):
                raise ValueError('Пользователь с таким email уже существует')
            
            # Хеширование пароля
            password_hash = User.hash_password(password)
            
            # Создание пользователя
            query = """
                INSERT INTO users (username, email, password_hash) 
                VALUES (%s, %s, %s)
            """
            user_id = db.execute_query(query, (username, email, password_hash))
            
            # Получаем созданного пользователя
            user = UserRepository.get_by_id(user_id)
            if not user:
                raise ValueError('Ошибка при создании пользователя')
            
            logger.info(f'Created new user with ID: {user_id}')
            return user
            
        except ValueError as e:
            raise e
        except Exception as e:
            logger.error(f'Error creating user: {str(e)}')
            raise ValueError('Ошибка при создании пользователя')
    
    @staticmethod
    def authenticate(username: str, password: str):
        """Аутентификация пользователя"""
        try:
            user = UserRepository.get_by_username(username)
            if user and user.check_password(password):
                return user
            return None
        except Exception as e:
            logger.error(f'Error authenticating user: {str(e)}')
            return None
    
    def get_user_profile(self, user_id):  
        """Получить профиль пользователя"""
        try:
            query = """
                SELECT id, username, email, first_name, gender, age, 
                height_cm, weight_kg, target_weight_kg, bio, created_at, updated_at 
                FROM users WHERE id = %s
            """
            result = self.db.execute_query(query, (user_id,))
            if result and len(result) > 0:
                return result[0]
            return None
        except Exception as e:
            print(f"Error getting user profile: {e}")
            return None


    def update_user_profile(self, user_id, profile_data):  
        """Обновить профиль пользователя"""
        try:
            query = """
                UPDATE users SET 
                first_name = %s,
                gender = %s,
                age = %s,
                height_cm = %s,
                weight_kg = %s,
                target_weight_kg = %s,
                bio = %s,
                updated_at = CURRENT_TIMESTAMP
                WHERE id = %s
            """
        
            self.db.execute_query(query, (
                profile_data.get('first_name'),
                profile_data.get('gender'),
                profile_data.get('age'),
                profile_data.get('height_cm'),
                profile_data.get('weight_kg'),
                profile_data.get('target_weight_kg'),
                profile_data.get('bio'),
                user_id
            ))
            return True
        except Exception as e:
            print(f"Error updating user profile: {e}")
            return False
        

