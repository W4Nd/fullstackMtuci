from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.v1 import get_api_router
from app.database import get_db
import logging

from app.api.v1.seo import router as seo_router

# Логирование
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="Medication Reminder API", 
    version="1.0.0"
)

# CORS для React (http://localhost:5173)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Подключаем API роутер
api_router = get_api_router()
app.include_router(api_router, prefix="/api/v1")
app.include_router(seo_router)

@app.on_event("startup")
async def startup_event():
    """Инициализация при запуске"""
    try:
        db = get_db()
        logger.info("🚀 Medication Reminder FastAPI запущен!")
        logger.info("✅ База данных готова")
        logger.info("📚 Swagger: http://localhost:8000/docs")
    except Exception as e:
        logger.error(f"❌ Startup failed: {e}")
        raise

@app.get("/")
async def root():
    return {"message": "Medication Reminder API 🚀", "version": "1.0.0"}

@app.get("/health")
async def health_check():
    return {"status": "healthy"}
