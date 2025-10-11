from dataclasses import dataclass, asdict
from datetime import time
from typing import List
import json

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