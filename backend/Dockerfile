FROM python:3.12-slim

WORKDIR /app

# Копируем requirements.txt из корня проекта
COPY requirements.txt .

# Устанавливаем зависимости (включая uvicorn)
RUN pip install --no-cache-dir -r requirements.txt

# Копируем код бэкенда
COPY backend/ .

# Создаем пользователя для безопасности
RUN useradd --create-home appuser && chown -R appuser:appuser /app

# Переключаемся на пользователя
USER appuser

EXPOSE 8000

# Запуск приложения
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]