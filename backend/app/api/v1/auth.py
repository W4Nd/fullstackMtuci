from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel
from typing import Optional
import jwt
from jwt.exceptions import PyJWTError
from app.core.security import (
    verify_password, create_access_token, create_refresh_token, 
    verify_refresh_token, revoke_refresh_token, hash_password, SECRET_KEY, ALGORITHM
)
from app.repositories.auth_repository import AuthRepository
from app.services.rbac_service import RBACService

router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/token")

class Token(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"

class RegisterRequest(BaseModel):
    username: str
    email: str
    password: str

# 3.1 ✅ LOGIN (access + refresh токены)
@router.post("/token", response_model=Token)
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    """Вход: access + refresh токены"""
    user = AuthRepository.get_user_by_username(form_data.username)
    if not user or not verify_password(form_data.password, user.password_hash):
        raise HTTPException(status_code=401, detail="Неверные данные")
    
    access_token = create_access_token({"sub": user.username, "user_id": user.id})
    refresh_token, jti = create_refresh_token(user.id)
    
    return Token(
        access_token=access_token,
        refresh_token=refresh_token,
        token_type="bearer"
    )

# 3.2 ✅ REFRESH (ротация токенов)
@router.post("/refresh", response_model=Token)
async def refresh_token_endpoint(refresh_token: str = Depends(oauth2_scheme)):
    """Обновление токенов (ротация refresh)"""
    payload = verify_refresh_token(refresh_token)
    if not payload:
        raise HTTPException(status_code=401, detail="Invalid refresh token")
    
    user_id = payload["sub"]
    access_token = create_access_token({"sub": payload.get("username", ""), "user_id": user_id})
    new_refresh_token, new_jti = create_refresh_token(user_id)
    revoke_refresh_token(payload["jti"])
    
    return Token(
        access_token=access_token,
        refresh_token=new_refresh_token,
        token_type="bearer"
    )

# 3.3 ✅ LOGOUT (отзыв refresh)
@router.post("/logout", status_code=204)
async def logout(token: str = Depends(oauth2_scheme)):
    """Выход: отзыв refresh токена"""
    payload = verify_refresh_token(token)
    if payload:
        revoke_refresh_token(payload["jti"])
    return None

# 3.4 ✅ ТЕКУЩИЙ ПОЛЬЗОВАТЕЛЬ
async def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        user_id: int = payload.get("user_id")
        if username is None or user_id is None:
            raise HTTPException(status_code=401, detail="Invalid token")
        return {"user_id": user_id, "username": username}
    except PyJWTError:
        raise HTTPException(status_code=401, detail="Invalid token")

@router.get("/me")
async def get_current_user_info(current_user: dict = Depends(get_current_user)):
    """Информация о текущем пользователе + роли"""
    user = AuthRepository.get_user_by_id(current_user["user_id"])
    roles = RBACService.get_user_roles(current_user["user_id"])
    return {
        "user": user.to_dict(),
        "roles": roles,
        "permissions": RBACService.get_all_permissions(roles)
    }

# REGISTER (совместимость с frontend)
@router.post("/register")
async def register(request: RegisterRequest):
    """Регистрация (для старого фронта)"""
    user = AuthRepository.get_user_by_username(request.username)
    if user:
        raise HTTPException(status_code=400, detail="Пользователь существует")
    
    user = AuthRepository.create_user(request.username, request.email, hash_password(request.password))
    access_token = create_access_token({"sub": user.username, "user_id": user.id})
    refresh_token, jti = create_refresh_token(user.id)
    
    return {
        "token": access_token,  # совместимость
        "access_token": access_token,
        "refresh_token": refresh_token,
        "user": user.to_dict(),
        "roles": RBACService.get_user_roles(user.id)
    }
