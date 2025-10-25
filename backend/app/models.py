from dataclasses import dataclass, asdict
from datetime import time
from typing import List, Optional
import json
import bcrypt

@dataclass
class User:
    id: int
    username: str
    email: str
    password_hash: str
    created_at: str
    
    @staticmethod
    def hash_password(password: str) -> str:
        return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
    
    def check_password(self, password: str) -> bool:
        return bcrypt.checkpw(password.encode('utf-8'), self.password_hash.encode('utf-8'))
    
    def to_dict(self) -> dict:
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'created_at': self.created_at
        }

@dataclass
class Medication:
    name: str
    dosage: str

@dataclass
class Reminder:
    id: int
    medication: Medication
    time: str 
    days: List[int] 
    is_active: bool = True
    
    def to_dict(self):
        return {
            'id': self.id,
            'medication': {
                'name': self.medication.name,
                'dosage': self.medication.dosage
            },
            'time': self.time,
            'days': self.days,
            'is_active': self.is_active
        }