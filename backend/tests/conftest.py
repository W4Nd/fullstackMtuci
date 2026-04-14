import pytest
import uuid
import os
import psycopg2
from psycopg2.extras import RealDictCursor
from fastapi.testclient import TestClient
from app.core.config import get_settings
from app.core.security import hash_password

# Загружаем тестовые переменные окружения
os.environ["DB_HOST"] = "localhost"
os.environ["DB_PORT"] = "5432"
os.environ["DB_USER"] = "postgres"
os.environ["DB_PASSWORD"] = "forz9r"
os.environ["DB_NAME"] = "medic_db_test"

class TestSettings:
    DEBUG = True
    SECRET_KEY = "test_secret"
    JWT_SECRET_KEY = "test_jwt_secret"
    ALGORITHM = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES = 15
    REFRESH_TOKEN_EXPIRE_DAYS = 7
    FDA_API_ENABLED = True
    FDA_API_TIMEOUT = 5
    DB_HOST = "localhost"
    DB_PORT = 5432
    DB_USER = "postgres"
    DB_PASSWORD = "forz9r"
    DB_NAME = "medic_db_test"

# Создаём тестовое соединение
_test_connection = None

def get_test_connection():
    global _test_connection
    if _test_connection is None or _test_connection.closed:
        _test_connection = psycopg2.connect(
            host=TestSettings.DB_HOST,
            port=TestSettings.DB_PORT,
            user=TestSettings.DB_USER,
            password=TestSettings.DB_PASSWORD,
            database=TestSettings.DB_NAME,
            cursor_factory=RealDictCursor
        )
        _test_connection.autocommit = True
    return _test_connection

@pytest.fixture(scope="session")
def setup_database():
    """Создаёт таблицы в тестовой БД (один раз)"""
    conn = psycopg2.connect(
        host=TestSettings.DB_HOST,
        port=TestSettings.DB_PORT,
        user=TestSettings.DB_USER,
        password=TestSettings.DB_PASSWORD,
        database=TestSettings.DB_NAME
    )
    conn.autocommit = True
    with conn.cursor() as cur:
        cur.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id SERIAL PRIMARY KEY,
                username VARCHAR(50) UNIQUE NOT NULL,
                email VARCHAR(100) UNIQUE NOT NULL,
                password_hash TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT NOW(),
                first_name VARCHAR(50),
                gender VARCHAR(10),
                age INTEGER,
                height_cm INTEGER,
                weight_kg REAL,
                target_weight_kg REAL,
                bio TEXT,
                updated_at TIMESTAMP
            );
            CREATE TABLE IF NOT EXISTS reminders (
                    id SERIAL PRIMARY KEY,
                    user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
                    medication_name VARCHAR(100) NOT NULL,
                    dosage VARCHAR(50) NOT NULL,
                    reminder_time TIME NOT NULL,
                    days JSONB NOT NULL,
                    is_active BOOLEAN DEFAULT TRUE,
                    created_at TIMESTAMP DEFAULT NOW()
                );
            CREATE TABLE IF NOT EXISTS refresh_tokens (
                id SERIAL PRIMARY KEY,
                user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
                token_hash TEXT NOT NULL,
                jti VARCHAR(36) NOT NULL,
                expires_at TIMESTAMP NOT NULL,
                revoked BOOLEAN DEFAULT FALSE
            );
        """)
    conn.close()

@pytest.fixture(scope="function")
def db_session(setup_database):
    """Очищает таблицы и возвращает соединение"""
    conn = get_test_connection()
    # Очищаем таблицы перед тестом
    with conn.cursor() as cur:
        cur.execute("TRUNCATE TABLE users, reminders, refresh_tokens RESTART IDENTITY CASCADE")
    yield conn

@pytest.fixture
def client(monkeypatch):
    """Тестовый клиент FastAPI с тестовой БД"""
    # Подменяем настройки
    monkeypatch.setattr("app.core.config.get_settings", lambda: TestSettings())
    
    # Перезагружаем модуль database, чтобы он использовал новые настройки
    import importlib
    import app.database
    importlib.reload(app.database)
    
    # Импортируем app после перезагрузки настроек
    from app.main import app
    
    with TestClient(app) as test_client:
        yield test_client

@pytest.fixture
def test_user(db_session):
    """Создаёт тестового пользователя"""
    unique_id = uuid.uuid4().hex[:8]
    username = f"testuser_{unique_id}"
    email = f"test_{unique_id}@example.com"
    password = "testpass"
    password_hash = hash_password(password)

    with db_session.cursor() as cur:
        cur.execute("""
            INSERT INTO users (username, email, password_hash, created_at)
            VALUES (%s, %s, %s, NOW())
            RETURNING *
        """, (username, email, password_hash))
        row = cur.fetchone()
        return dict(row)

@pytest.fixture
def auth_headers(client, test_user):
    """Возвращает заголовки авторизации"""
    response = client.post(
        "/api/v1/auth/token",
        data={"username": test_user["username"], "password": "testpass"}
    )
    assert response.status_code == 200, f"Login failed: {response.text}"
    token = response.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}
    
@pytest.fixture
def reminder(client, auth_headers):
    """Создаёт тестовое напоминание"""
    payload = {
        "medication_name": "Aspirin",
        "dosage": "100mg",
        "time": "08:00",
        "days": [1, 3, 5]
    }
    response = client.post("/api/v1/reminders", json=payload, headers=auth_headers)
    # 🔧 Принимаем 200 или 201
    assert response.status_code in [200, 201], f"Failed to create reminder: {response.text}"
    return response.json()

@pytest.fixture
def other_user(db_session):
    """Создаёт другого пользователя для тестов доступа"""
    unique_id = uuid.uuid4().hex[:8]
    username = f"otheruser_{unique_id}"
    email = f"other_{unique_id}@example.com"
    password = "otherpass"
    password_hash = hash_password(password)

    with db_session.cursor() as cur:
        cur.execute("""
            INSERT INTO users (username, email, password_hash, created_at)
            VALUES (%s, %s, %s, NOW())
            RETURNING *
        """, (username, email, password_hash))
        row = cur.fetchone()
        return dict(row)

@pytest.fixture
def other_user_auth_headers(client, other_user):
    """Заголовки авторизации для другого пользователя"""
    response = client.post(
        "/api/v1/auth/token",
        data={"username": other_user["username"], "password": "otherpass"}
    )
    assert response.status_code == 200
    token = response.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}

@pytest.fixture
def other_user_reminder(client, other_user_auth_headers):
    """Напоминание другого пользователя"""
    payload = {
        "medication_name": "Ibuprofen",
        "dosage": "200mg",
        "time": "09:00",
        "days": [2, 4]
    }
    response = client.post("/api/v1/reminders", json=payload, headers=other_user_auth_headers)
    assert response.status_code == 200
    return response.json()