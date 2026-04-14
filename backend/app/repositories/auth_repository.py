from app.database import get_db
from app.models import User

class AuthRepository:
    @staticmethod
    def get_user_by_username(username: str):
        db = get_db()
        result = db.execute_query("SELECT * FROM users WHERE username = %s", (username,))
        return User.from_db(result[0]) if result else None
    
    @staticmethod
    def create_user(username: str, email: str, password_hash: str):
        db = get_db()
        db.execute_query("""
            INSERT INTO users (username, email, password_hash) 
            VALUES (%s, %s, %s) RETURNING id
        """, (username, email, password_hash))
        return AuthRepository.get_user_by_username(username)
    
    @staticmethod
    def get_user_roles(user_id: int):
        db = get_db()
        result = db.execute_query("""
            SELECT r.name, r.permissions 
            FROM user_roles ur 
            JOIN roles r ON ur.role_id = r.id 
            WHERE ur.user_id = %s
        """, (user_id,))
        return [row["permissions"] for row in result] if result else []
        
    @staticmethod
    def get_user_by_id(user_id: int):
        db = get_db()
        result = db.execute_query("SELECT * FROM users WHERE id = %s", (user_id,))
        return User.from_db(result[0]) if result else None
