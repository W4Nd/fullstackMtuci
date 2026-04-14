from fastapi import APIRouter, Depends, Query, HTTPException
from app.services.weather_service import WeatherService 
from app.core.config import settings

router = APIRouter()

def get_weather_service() -> WeatherService:
    return WeatherService()

@router.get("/weather/current")
async def get_current_weather(
    lat: float = Query(..., description="Широта (например, 55.75)"),
    lon: float = Query(..., description="Долгота (например, 37.61)"),
    weather_service: WeatherService = Depends(get_weather_service)
):
    """Получить текущую погоду (пример интеграции)"""
    result = await weather_service.get_weather(lat, lon)
    
    if not result["success"]:
        status = 504 if result["error"] == "timeout" else 502
        raise HTTPException(status_code=status, detail=result["message"])
    
    return result