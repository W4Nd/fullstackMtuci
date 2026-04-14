# backend/app/services/weather_service.py
import httpx
import logging
from app.core.config import settings

logger = logging.getLogger(__name__)

class WeatherService:
    """Сервис для получения погоды (замена FDA для стабильности)"""
    
    BASE_URL = "https://api.open-meteo.com/v1/forecast"
    
    def __init__(self):
        self.timeout = httpx.Timeout(10.0)
        # Обязательный User-Agent для большинства бесплатных API
        self.headers = {"User-Agent": "MedicationReminderApp/1.0"}
    
    async def get_weather(self, latitude: float, longitude: float) -> dict:
        """Получить текущую погоду по координатам"""
        params = {
            "latitude": latitude,
            "longitude": longitude,
            "current_weather": True
        }
        
        try:
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                response = await client.get(
                    self.BASE_URL, 
                    params=params, 
                    headers=self.headers
                )
                
                if response.status_code != 200:
                    logger.error(f"Weather API error: {response.status_code}")
                    return {"success": False, "error": "api_error", "message": "Ошибка получения погоды"}

                data = response.json()
                
                weather = data.get("current_weather", {})
                
                return {
                    "success": True,
                    "location": f"{latitude}, {longitude}",
                    "temperature": weather.get("temperature"),
                    "wind_speed": weather.get("windspeed"),
                    "description": f"Температура: {weather.get('temperature')}°C, Ветер: {weather.get('windspeed')} км/ч"
                }
                
        except httpx.TimeoutException:
            logger.error("Weather API timeout")
            return {"success": False, "error": "timeout", "message": "Превышено время ожидания ответа от погодного сервиса"}
        except Exception as e:
            logger.exception(f"Unexpected error: {e}")
            return {"success": False, "error": "internal", "message": "Внутренняя ошибка"}