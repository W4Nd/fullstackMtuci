from flask import request, jsonify
from app.api import bp
from app.repositories.reminder_repository import ReminderRepository
from app.validation.validators import validate_reminder_data
import logging

logger = logging.getLogger(__name__)

@bp.route('/reminders', methods=['GET'])
def get_reminders():
    """Получить все напоминания"""
    try:
        logger.info('Fetching all reminders')
        reminders = ReminderRepository.get_all()
        return jsonify([reminder.to_dict() for reminder in reminders])
    except Exception as e:
        logger.error(f'Error fetching reminders: {str(e)}')
        return jsonify({'error': 'Internal server error'}), 500

@bp.route('/reminders', methods=['POST'])
def create_reminder():
    """Создать новое напоминание"""
    try:
        data = request.json
        
        # Валидация данных
        validation_errors = validate_reminder_data(data)
        if validation_errors:
            logger.warning(f'Validation errors: {validation_errors}')
            return jsonify({'errors': validation_errors}), 400
        
        logger.info(f'Creating new reminder: {data}')
        
        # Создание напоминания
        reminder = ReminderRepository.create(
            medication_name=data['medication_name'],
            dosage=data['dosage'],
            time=data['time'],
            days=data['days']
        )
        
        return jsonify(reminder.to_dict()), 201
        
    except Exception as e:
        logger.error(f'Error creating reminder: {str(e)}')
        return jsonify({'error': 'Internal server error'}), 500

@bp.route('/reminders/<int:reminder_id>', methods=['DELETE'])
def delete_reminder(reminder_id):
    """Удалить напоминание"""
    try:
        logger.info(f'Deleting reminder with ID: {reminder_id}')
        
        success = ReminderRepository.delete(reminder_id)
        if not success:
            return jsonify({'error': 'Reminder not found'}), 404
            
        return jsonify({'message': 'Reminder deleted successfully'}), 200
        
    except Exception as e:
        logger.error(f'Error deleting reminder: {str(e)}')
        return jsonify({'error': 'Internal server error'}), 500

@bp.route('/reminders/<int:reminder_id>/toggle', methods=['POST'])
def toggle_reminder(reminder_id):
    """Переключить статус напоминания"""
    try:
        logger.info(f'Toggling reminder with ID: {reminder_id}')
        
        reminder = ReminderRepository.toggle(reminder_id)
        if not reminder:
            return jsonify({'error': 'Reminder not found'}), 404
            
        return jsonify(reminder.to_dict()), 200
        
    except Exception as e:
        logger.error(f'Error toggling reminder: {str(e)}')
        return jsonify({'error': 'Internal server error'}), 500

@bp.route('/reminders/test-notification', methods=['POST'])
def test_notification():
    """Тестовый endpoint для уведомлений"""
    try:
        from app.services.notification_service import NotificationService
        service = NotificationService()
        service.check_reminders()
        return jsonify({'message': 'Notification test completed'}), 200
    except Exception as e:
        logger.error(f'Error testing notifications: {str(e)}')
        return jsonify({'error': 'Internal server error'}), 500