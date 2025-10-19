import json
import os
from app.models import Reminder, Medication
import logging

logger = logging.getLogger(__name__)

DATA_FILE = 'data/reminders.json'

def load_reminders():
    """Загружает напоминания из файла"""
    if not os.path.exists(DATA_FILE):
        logger.info('Data file not found, returning empty list')
        return []
    
    try:
        with open(DATA_FILE, 'r', encoding='utf-8') as f:
            data = json.load(f)
            reminders = []
            for item in data:
                try:
                    medication = Medication(
                        name=item['medication']['name'],
                        dosage=item['medication']['dosage']
                    )
                    reminder = Reminder(
                        id=item['id'],
                        medication=medication,
                        time=item['time'],
                        days=item['days'],
                        is_active=item.get('is_active', True)
                    )
                    reminders.append(reminder)
                except KeyError as e:
                    logger.warning(f'Skipping invalid reminder data: {e}')
                    continue
            
            logger.info(f'Loaded {len(reminders)} reminders from storage')
            return reminders
            
    except (json.JSONDecodeError, Exception) as e:
        logger.error(f'Error loading reminders from {DATA_FILE}: {str(e)}')
        return []

def save_reminders(reminders):
    """Сохраняет напоминания в файл"""
    try:
        os.makedirs(os.path.dirname(DATA_FILE), exist_ok=True)
        
        with open(DATA_FILE, 'w', encoding='utf-8') as f:
            json.dump([reminder.to_dict() for reminder in reminders], f, 
                     indent=2, ensure_ascii=False)
        
        logger.info(f'Saved {len(reminders)} reminders to storage')
        return True
        
    except Exception as e:
        logger.error(f'Error saving reminders to {DATA_FILE}: {str(e)}')
        return False