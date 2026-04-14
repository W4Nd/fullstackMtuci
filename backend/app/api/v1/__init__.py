from fastapi import APIRouter

from .auth import router as auth_router
from .profile import router as profile_router
from .reminders import router as reminders_router
from .reminder_files import router as reminder_files_router
from .external import router as ext_router

api_router = APIRouter()

# Подключаем только auth (остальные добавим после создания)
api_router.include_router(auth_router, prefix="/auth", tags=["auth"])
api_router.include_router(profile_router, prefix="/profile", tags=["profile"])
api_router.include_router(reminders_router, prefix="/reminders", tags=["reminders"])
api_router.include_router(reminder_files_router, prefix="/reminders", tags=["reminder_files"])
api_router.include_router(ext_router, prefix="/external", tags=["external_apis"])

# Функция для подключения в main.py
def get_api_router():
    return api_router
