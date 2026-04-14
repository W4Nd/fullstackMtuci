import pytest
from app.models import User, Reminder, Medication
from app.core.security import hash_password, verify_password, create_access_token, create_refresh_token
from datetime import datetime, timedelta
import jwt
from app.core.config import get_settings
import json

def test_hash_and_verify_password():
    password = "mysecret123"
    hashed = hash_password(password)
    assert hashed != password
    assert verify_password(password, hashed)
    assert not verify_password("wrong", hashed)

def test_hash_long_password():
    long_password = "a" * 100
    hashed = hash_password(long_password)
    assert verify_password(long_password, hashed)

def test_user_model():
    user_data = {
        "id": 1,
        "username": "john",
        "email": "john@example.com",
        "password_hash": hash_password("pass"),
        "created_at": "2025-01-01T12:00:00",
        "first_name": "John",
        "age": 30,
        "height_cm": 180,
        "weight_kg": 75,
    }
    user = User.from_db(user_data)
    assert user.username == "john"
    assert user.calculate_bmi() == pytest.approx(23.15, 0.01)
    assert user.check_password("pass")
    assert not user.check_password("wrong")
    d = user.to_dict()
    assert d["bmi"] == 23.15

def test_reminder_model():
    row = {
        "id": 1,
        "user_id": 1,
        "medication_name": "Aspirin",
        "dosage": "100mg",
        "reminder_time": "08:30",
        "days": json.dumps([0,2,4]),
        "is_active": True
    }
    rem = Reminder.from_db(row)
    assert rem.medication.name == "Aspirin"
    assert rem.time == "08:30"
    assert rem.days == [0,2,4]
    assert rem.to_dict()["medication"]["dosage"] == "100mg"

def test_create_access_token():
    data = {"sub": 1}
    token = create_access_token(data)
    decoded = jwt.decode(token, get_settings().SECRET_KEY, algorithms=["HS256"])
    assert decoded["sub"] == 1
    assert "exp" in decoded
    assert decoded["type"] == "access"