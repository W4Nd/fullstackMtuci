import json
import os
from app.models import Reminder, Medication

DATA_FILE = 'data/reminders.json'

def load_reminders():
    if not os.path.exists(DATA_FILE):
        return []
    
    try:
        with open(DATA_FILE, 'r', encoding='utf-8') as f:
            data = json.load(f)
            reminders = []
            for item in data:
                medication = Medication(
                    name=item['medication']['name'],
                    dosage=item['medication']['dosage']
                )
                reminder = Reminder(
                    id=item['id'],
                    medication=medication,
                    time=item['time'],
                    days=item['days'],
                    is_active=item['is_active']
                )
                reminders.append(reminder)
            return reminders
    except Exception as e:
        print(f"Error loading reminders: {e}")
        return []

def save_reminders(reminders):
    try:
        with open(DATA_FILE, 'w', encoding='utf-8') as f:
            json.dump([reminder.to_dict() for reminder in reminders], f, indent=2, ensure_ascii=False)
        return True
    except Exception as e:
        print(f"Error saving reminders: {e}")
        return False

def get_next_id(reminders):
    return max([r.id for r in reminders], default=0) + 1