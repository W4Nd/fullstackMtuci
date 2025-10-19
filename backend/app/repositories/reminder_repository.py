import json
import os
from app.models import Reminder, Medication
from app.storage import load_reminders, save_reminders
import logging

logger = logging.getLogger(__name__)

class ReminderRepository:
    """Репозиторий для работы с напоминаниями"""
    
    @staticmethod
    def get_all():
        """Получить все напоминания"""
        return load_reminders()
    
    @staticmethod
    def get_by_id(reminder_id):
        """Получить напоминание по ID"""
        reminders = load_reminders()
        for reminder in reminders:
            if reminder.id == reminder_id:
                return reminder
        return None
    
    @staticmethod
    def create(medication_name, dosage, time, days):
        """Создать новое напоминание"""
        reminders = load_reminders()
        
        # Генерация нового ID
        new_id = max([r.id for r in reminders], default=0) + 1
        
        # Создание объектов
        medication = Medication(name=medication_name, dosage=dosage)
        reminder = Reminder(
            id=new_id,
            medication=medication,
            time=time,
            days=days,
            is_active=True
        )
        
        # Сохранение
        reminders.append(reminder)
        save_reminders(reminders)
        
        logger.info(f'Created new reminder with ID: {new_id}')
        return reminder
    
    @staticmethod
    def delete(reminder_id):
        """Удалить напоминание"""
        reminders = load_reminders()
        initial_count = len(reminders)
        
        reminders = [r for r in reminders if r.id != reminder_id]
        
        if len(reminders) < initial_count:
            save_reminders(reminders)
            logger.info(f'Deleted reminder with ID: {reminder_id}')
            return True
        
        logger.warning(f'Attempted to delete non-existent reminder with ID: {reminder_id}')
        return False
    
    @staticmethod
    def toggle(reminder_id):
        """Переключить статус напоминания"""
        reminders = load_reminders()
        
        for reminder in reminders:
            if reminder.id == reminder_id:
                reminder.is_active = not reminder.is_active
                save_reminders(reminders)
                logger.info(f'Toggled reminder with ID: {reminder_id} to {reminder.is_active}')
                return reminder
        
        logger.warning(f'Attempted to toggle non-existent reminder with ID: {reminder_id}')
        return None
    
    @staticmethod
    def update(reminder_id, **kwargs):
        """Обновить напоминание"""
        reminders = load_reminders()
        
        for reminder in reminders:
            if reminder.id == reminder_id:
                if 'medication_name' in kwargs:
                    reminder.medication.name = kwargs['medication_name']
                if 'dosage' in kwargs:
                    reminder.medication.dosage = kwargs['dosage']
                if 'time' in kwargs:
                    reminder.time = kwargs['time']
                if 'days' in kwargs:
                    reminder.days = kwargs['days']
                
                save_reminders(reminders)
                logger.info(f'Updated reminder with ID: {reminder_id}')
                return reminder
        
        logger.warning(f'Attempted to update non-existent reminder with ID: {reminder_id}')
        return None