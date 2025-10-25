import schedule
import time
import threading
import logging
from datetime import datetime
from app.repositories.reminder_repository import ReminderRepository

logger = logging.getLogger(__name__)

class NotificationService:
    """Служба уведомлений о напоминаниях"""
    
    def __init__(self):
        self.is_running = False
        self.thread = None
        
    def check_reminders(self):
        """Проверяет активные напоминания для текущего времени"""
        try:
            current_time = datetime.now().strftime("%H:%M")
            current_day = datetime.now().weekday()
            
            reminders = ReminderRepository.get_all()
            active_reminders = []
            
            for reminder in reminders:
                if (reminder.time == current_time and 
                    current_day in reminder.days and 
                    reminder.is_active):
                    active_reminders.append(reminder)
            
            if active_reminders:
                self.send_notifications(active_reminders)
                
        except Exception as e:
            logger.error(f'Error checking reminders: {str(e)}')
    
    def send_notifications(self, reminders):
        """Отправляет уведомления для списка напоминаний"""
        for reminder in reminders:
            message = self.format_notification_message(reminder)
            self.send_notification(message, reminder)
    
    def format_notification_message(self, reminder):
        """Форматирует сообщение уведомления"""
        day_names = ['Пн', 'Вт', 'Ср', 'Чт', 'Пт', 'Сб', 'Вс']
        days_str = ', '.join([day_names[d] for d in reminder.days])
        
        return (f"💊 Время принять {reminder.medication.name} - {reminder.medication.dosage}\n"
                f"⏰ Время: {reminder.time}\n"
                f"📅 Дни: {days_str}")
    
    def send_notification(self, message, reminder):
        """Отправляет одно уведомление"""
        logger.info(f"NOTIFICATION: {message}")
        print(f"\n🔔 УВЕДОМЛЕНИЕ: {message}\n")
    
    def start_scheduler(self):
        """Запускает планировщик в отдельном потоке"""
        if self.is_running:
            logger.warning('Notification service is already running')
            return
        
        self.is_running = True
        
        # Настройка расписания
        schedule.every(1).minutes.do(self.check_reminders)
        
        def run_scheduler():
            logger.info('Notification scheduler started')
            while self.is_running:
                try:
                    schedule.run_pending()
                    time.sleep(1)
                except Exception as e:
                    logger.error(f'Error in scheduler loop: {str(e)}')
                    time.sleep(5)
        
        self.thread = threading.Thread(target=run_scheduler)
        self.thread.daemon = True
        self.thread.start()
        logger.info('Notification service started successfully')
    
    def stop_scheduler(self):
        """Останавливает планировщик"""
        if not self.is_running:
            return
    
        self.is_running = False
        schedule.clear()  # Очищаем все запланированные задачи
    
        if self.thread:
            self.thread.join(timeout=3)  # Ждем завершения потока (макс 3 сек)
            print('🔔 Служба уведомлений остановлена')