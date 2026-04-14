import json
import logging
from dataclasses import dataclass
from typing import List, Optional

import bcrypt

logger = logging.getLogger(__name__)


@dataclass
class User:
    id: int
    username: str
    email: str
    password_hash: str
    created_at: str
    first_name: Optional[str] = None
    gender: Optional[str] = None
    age: Optional[int] = None
    height_cm: Optional[int] = None
    weight_kg: Optional[float] = None
    target_weight_kg: Optional[float] = None
    bio: Optional[str] = None
    updated_at: Optional[str] = None

    @staticmethod
    def hash_password(password: str) -> str:
        return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")

    def check_password(self, password: str) -> bool:
        return bcrypt.checkpw(
            password.encode("utf-8"), self.password_hash.encode("utf-8")
        )

    def calculate_bmi(self) -> Optional[float]:
        """Рассчитывает ИМТ (BMI)"""
        if self.height_cm and self.weight_kg:
            height_m = self.height_cm / 100
            bmi = self.weight_kg / (height_m**2)
            return round(bmi, 2)
        return None

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "username": self.username,
            "email": self.email,
            "first_name": self.first_name,
            "gender": self.gender,
            "age": self.age,
            "height_cm": self.height_cm,
            "weight_kg": self.weight_kg,
            "target_weight_kg": self.target_weight_kg,
            "bio": self.bio,
            "bmi": self.calculate_bmi(),
            "created_at": self.created_at,
            "updated_at": self.updated_at,
        }

    @classmethod
    def from_db(cls, db_row: dict):
        """Создать объект User из строки базы данных"""
        return cls(
            id=db_row["id"],
            username=db_row["username"],
            email=db_row["email"],
            password_hash=db_row["password_hash"],
            created_at=db_row["created_at"].isoformat()
            if hasattr(db_row["created_at"], "isoformat")
            else db_row["created_at"],
            first_name=db_row.get("first_name"),
            gender=db_row.get("gender"),
            age=db_row.get("age"),
            height_cm=db_row.get("height_cm"),
            weight_kg=db_row.get("weight_kg"),
            target_weight_kg=db_row.get("target_weight_kg"),
            bio=db_row.get("bio"),
            updated_at=db_row.get("updated_at").isoformat()
            if db_row.get("updated_at")
            and hasattr(db_row.get("updated_at"), "isoformat")
            else db_row.get("updated_at"),
        )


@dataclass
class Medication:
    name: str
    dosage: str


@dataclass
class Reminder:
    id: int
    user_id: int
    medication: Medication
    time: str  # логическое имя, в БД колонка reminder_time
    days: List[int]
    is_active: bool = True

    def to_dict(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "medication": {
                "name": self.medication.name,
                "dosage": self.medication.dosage,
            },
            "time": str(self.time),
            "days": self.days,
            "is_active": self.is_active,
        }

    @classmethod
    def from_db(cls, db_row: dict):
        """Создать объект Reminder из строки базы данных"""
        try:
            days = db_row["days"]
            if isinstance(days, str):
                try:
                    days = json.loads(days)
                except json.JSONDecodeError:
                    logger.error(f"Invalid JSON in days field: {days}")
                    days = []
            elif days is None:
                days = []

            time_value = db_row.get("reminder_time") or db_row.get("time")
            if hasattr(time_value, "strftime"):
                time_str = time_value.strftime("%H:%M")
            else:
                time_str = str(time_value) if time_value is not None else ""

            return cls(
                id=db_row["id"],
                user_id=db_row["user_id"],
                medication=Medication(
                    name=db_row["medication_name"],
                    dosage=db_row["dosage"],
                ),
                time=time_str,
                days=days,
                is_active=bool(db_row.get("is_active", True)),
            )
        except Exception as e:
            logger.error(f"Error creating Reminder from DB row: {e}")
            raise
            
@dataclass
class Role:
    id: int
    name: str
    description: str
    permissions: List[str]

    @classmethod
    def from_db(cls, db_row: dict):
        return cls(
            id=db_row["id"],
            name=db_row["name"],
            description=db_row["description"],
            permissions=json.loads(db_row["permissions"])
        )
