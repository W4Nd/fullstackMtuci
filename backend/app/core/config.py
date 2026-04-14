# backend/app/core/config.py
from pydantic_settings import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):
    """Основные настройки приложения"""

    # Приложение
    APP_NAME: str = "Medication Reminder"
    VERSION: str = "1.0.0"
    DEBUG: bool = True
    
    # Бэкенд
    HOST: str = "0.0.0.0"
    PORT: int = 8000
    
    DB_HOST: str = "localhost"
    DB_PORT: int = 5432
    DB_USER: str = "postgres"
    DB_PASSWORD: str = "forz9r"
    DB_NAME: str = "medic_db"
    
    @property
    def DATABASE_URL(self) -> str:
        return f"postgresql://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"
    
    # CORS
    CORS_ORIGINS: list[str] = [
        "http://localhost:5173",
        "http://localhost:3000",
        "http://127.0.0.1:5173",
        "http://127.0.0.1:3000",
    ]
    
    # Безопасность
    SECRET_KEY: str = "6a6363668bcbb736406b4787d2145250f96ff9ccf2a9fb19ce2c80a1f06b3efe"
    JWT_SECRET_KEY: str ="ilx4BtGLljGrBECYrsTJ9JXyr+56LV7IgHnAmaWrrWc="
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7 
    
    # Внешние API
    FDA_API_ENABLED: bool = True
    FDA_API_TIMEOUT: int = 10 
    VITE_SITE_URL: str = "http://localhost:5173"
    
    class Config:
        env_file = ".env"
        case_sensitive = True


@lru_cache()
def get_settings() -> Settings:
    """Кэшированный доступ к настройкам"""
    return Settings()


settings = get_settings()