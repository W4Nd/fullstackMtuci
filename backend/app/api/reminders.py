from flask import request, jsonify, g
from app.api import bp
from app.repositories.reminder_repository import ReminderRepository
from app.validation.validators import validate_reminder_data
from app.middleware.auth_middleware import token_required, get_current_user_id
import logging

logger = logging.getLogger(__name__)

@bp.route('/reminders', methods=['GET', 'OPTIONS'])
@token_required
def get_reminders():
    """Получить все напоминания ТЕКУЩЕГО пользователя"""
    if request.method == 'OPTIONS':
        return '', 200
        
    try:
        user_id = get_current_user_id()
        logger.info(f'Fetching reminders for user: {user_id}')
        
        reminders = ReminderRepository.get_all(user_id=user_id)
        return jsonify([reminder.to_dict() for reminder in reminders])
    except Exception as e:
        logger.error(f'Error fetching reminders: {str(e)}')
        return jsonify({'error': 'Internal server error'}), 500

@bp.route('/reminders', methods=['POST', 'OPTIONS'])
@token_required
def create_reminder():
    """Создать новое напоминание для ТЕКУЩЕГО пользователя"""
    if request.method == 'OPTIONS':
        return '', 200
        
    try:
        user_id = get_current_user_id()
        data = request.json
        
        logger.info(f"📝 Creating reminder for user {user_id} with data: {data}")
        
        # Валидация данных
        validation_errors = validate_reminder_data(data)
        if validation_errors:
            logger.warning(f'Validation errors: {validation_errors}')
            return jsonify({'errors': validation_errors}), 400
        
        # Проверяем, что у нас есть user_id
        if not user_id:
            logger.error("No user_id in request context")
            return jsonify({'error': 'User not authenticated'}), 401
        
        logger.info(f'Creating new reminder for user {user_id}: {data}')
        
        # Создание напоминания
        reminder = ReminderRepository.create(
            user_id=user_id,
            medication_name=data['medication_name'],
            dosage=data['dosage'],
            time=data['time'],
            days=data['days']
        )
        
        logger.info(f'✅ Successfully created reminder: {reminder.id}')
        return jsonify(reminder.to_dict()), 201
        
    except Exception as e:
        logger.error(f'❌ Error creating reminder: {str(e)}', exc_info=True)
        return jsonify({'error': 'Internal server error'}), 500

@bp.route('/reminders/<int:reminder_id>', methods=['DELETE', 'OPTIONS'])
@token_required
def delete_reminder(reminder_id):
    """Удалить напоминание ТЕКУЩЕГО пользователя"""
    if request.method == 'OPTIONS':
        return '', 200
        
    try:
        user_id = get_current_user_id()
        logger.info(f'Deleting reminder with ID: {reminder_id} for user: {user_id}')
        
        success = ReminderRepository.delete(reminder_id, user_id=user_id)
        if not success:
            return jsonify({'error': 'Reminder not found'}), 404
            
        return jsonify({'message': 'Reminder deleted successfully'}), 200
        
    except Exception as e:
        logger.error(f'Error deleting reminder: {str(e)}')
        return jsonify({'error': 'Internal server error'}), 500

@bp.route('/reminders/<int:reminder_id>/toggle', methods=['POST', 'OPTIONS'])
@token_required
def toggle_reminder(reminder_id):
    """Переключить статус напоминания ТЕКУЩЕГО пользователя"""
    if request.method == 'OPTIONS':
        return '', 200
        
    try:
        user_id = get_current_user_id()
        logger.info(f'Toggling reminder with ID: {reminder_id} for user: {user_id}')
        
        reminder = ReminderRepository.toggle(reminder_id, user_id=user_id)
        if not reminder:
            return jsonify({'error': 'Reminder not found'}), 404
            
        return jsonify(reminder.to_dict()), 200
        
    except Exception as e:
        logger.error(f'Error toggling reminder: {str(e)}')
        return jsonify({'error': 'Internal server error'}), 500