# app/dependencies.py
from app.database import get_db

def get_db_dependency():
    return get_db()