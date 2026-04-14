from datetime import datetime, timedelta, timezone
from typing import Optional, Tuple
import jwt
from jwt.exceptions import PyJWTError
import bcrypt
import hashlib
import base64
import os
from dotenv import load_dotenv
import uuid
from app.database import get_db

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 15
REFRESH_TOKEN_EXPIRE_DAYS = 7

def hash_password(password: str) -> str:
    """Безопасное хеширование длинных паролей"""
    if len(password.encode('utf-8')) > 72:
        pre_hash = hashlib.sha256(password.encode('utf-8')).digest()
        password_bytes = base64.b64encode(pre_hash)[:72]  
    else:
        password_bytes = password.encode('utf-8')[:72]
    
    return bcrypt.hashpw(password_bytes, bcrypt.gensalt()).decode('utf-8')

def verify_password(plain_password: str, hashed: str) -> bool:
    """Проверка пароля"""
    if len(plain_password.encode('utf-8')) > 72:
        pre_hash = hashlib.sha256(plain_password.encode('utf-8')).digest()
        password_bytes = base64.b64encode(pre_hash)[:72]
    else:
        password_bytes = plain_password.encode('utf-8')[:72]
    
    return bcrypt.checkpw(password_bytes, hashed.encode('utf-8'))

def create_access_token(data: dict) -> str:
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire, "type": "access"})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def create_refresh_token(user_id: int) -> Tuple[str, str]:
    jti = str(uuid.uuid4())
    token_data = {
        "sub": user_id,
        "type": "refresh", 
        "jti": jti,
        "exp": datetime.now(timezone.utc) + timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)
    }
    refresh_token = jwt.encode(token_data, SECRET_KEY, algorithm=ALGORITHM)
    
    db = get_db()
    token_hash = hash_password(refresh_token) 
    expires_at = token_data["exp"]
    
    db.execute_query("""
        INSERT INTO refresh_tokens (user_id, token_hash, jti, expires_at) 
        VALUES (%s, %s, %s, %s)
    """, (user_id, token_hash, jti, expires_at))
    
    return refresh_token, jti

def verify_refresh_token(token: str) -> Optional[dict]:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        if payload.get("type") != "refresh":
            return None
        
        db = get_db()
        result = db.execute_query("""
            SELECT * FROM refresh_tokens 
            WHERE jti = %s AND revoked = FALSE AND expires_at > NOW()
        """, (payload["jti"],))
        
        if not result:
            return None
        
        stored_hash = result[0]["token_hash"]
        return payload if verify_password(token, stored_hash) else None
        
    except PyJWTError:
        return None

def revoke_refresh_token(jti: str):
    db = get_db()
    db.execute_query("UPDATE refresh_tokens SET revoked = TRUE WHERE jti = %s", (jti,))
