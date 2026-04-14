from fastapi import APIRouter, Depends, HTTPException
from app.api.v1.auth import get_current_user
from app.services.profile_service import ProfileService
from app.repositories.user_repository import UserRepository
from app.database import get_db
from app.services.rbac_service import RBACService

router = APIRouter()

def get_profile_service():
    return ProfileService(UserRepository(get_db()))

def get_rbac_service():
    return RBACService()

@router.get("/me")
async def get_profile(
    current_user: dict = Depends(get_current_user),
    profile_service: ProfileService = Depends(get_profile_service),
    rbac: RBACService = Depends(get_rbac_service)
):
    """Получить мой профиль (3.5 RBAC проверка)"""
    if not rbac.has_permission(
        rbac.get_user_roles(current_user["user_id"]), 
        "user:read_own"
    ):
        raise HTTPException(403, "Недостаточно прав")
    
    profile = profile_service.get_profile(current_user["user_id"])
    if not profile:
        raise HTTPException(404, "Profile not found")
    return profile

@router.put("/me")
async def update_profile(
    profile_data: dict,
    current_user: dict = Depends(get_current_user),
    profile_service: ProfileService = Depends(get_profile_service),
    rbac: RBACService = Depends(get_rbac_service)
):
    """Обновить профиль (RBAC user:update_own)"""
    if not rbac.has_permission(
        rbac.get_user_roles(current_user["user_id"]), 
        "user:update_own"
    ):
        raise HTTPException(403, "Недостаточно прав")
    
    result = profile_service.update_profile(current_user["user_id"], profile_data)
    if not result['success']:
        raise HTTPException(400, detail=result['errors'])
    
    return result
