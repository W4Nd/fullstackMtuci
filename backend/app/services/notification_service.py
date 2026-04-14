import schedule
import time
import threading
from datetime import datetime
from app.repositories.reminder_repository import ReminderRepository
import logging

logger = logging.getLogger(__name__)

class NotificationService:
    def __init__(self):
        self.scheduler_running = False
        self.scheduler_thread = None
    
    def check_reminders(self):
        """Проверить напоминания и отправить уведомления"""
        try:
            current_time = datetime.now().strftime('%H:%M')
            current_day = datetime.now().weekday()  
            
            logger.info(f'🔔 Checking reminders at {current_time}, day {current_day}')
            
            reminders = ReminderRepository.get_active_reminders()
            
            for reminder in reminders:
                reminder_time = reminder.time
                reminder_days = reminder.days
                
                # Проверяем совпадение времени и дня
                if (reminder_time == current_time and 
                    current_day in reminder_days):
                    
                    message = f"💊 Пора принять {reminder.medication.name} - {reminder.medication.dosage}"
                    logger.info(f'🚨 REMINDER: {message}')
                    
            
        except Exception as e:
            logger.error(f'Error checking reminders: {str(e)}')
    
    def start_scheduler(self):
        """Запустить планировщик в отдельном потоке"""
        if self.scheduler_running:
            logger.info('Scheduler is already running')
            return
        
        self.scheduler_running = True
        
        schedule.every(1).minutes.do(self.check_reminders)
        
        def run_scheduler():
            while self.scheduler_running:
                schedule.run_pending()
                time.sleep(1)
        
        self.scheduler_thread = threading.Thread(target=run_scheduler, daemon=True)
        self.scheduler_thread.start()
        logger.info('✅ Notification scheduler started')
    
    def stop_scheduler(self):
        """Остановить планировщик"""
        self.scheduler_running = False
        if self.scheduler_thread:
            self.scheduler_thread.join(timeout=5)
        logger.info('🛑 Notification scheduler stopped')
    
    def test_notification(self):
        """Тестовая функция для ручной проверки уведомлений"""
        logger.info('🧪 Running test notification')
        self.check_reminders()