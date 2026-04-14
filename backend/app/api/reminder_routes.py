from flask import Blueprint, request, jsonify, g
from app.middleware.auth_middleware import token_required
from app.middleware.rbac_middleware import require_permission
from app.repositories.reminder_repository import ReminderRepository
from app.database import get_db

reminders_bp = Blueprint('reminders', __name__, url_prefix='/api/v1/reminders')

@reminders_bp.route('/', methods=['GET'])
@token_required
@require_permission("reminder:read_own")
def get_reminders():
    user_id = g.user_id
    reminders = ReminderRepository.get_all(user_id)
    return jsonify([r.to_dict() for r in reminders])

@reminders_bp.route('/', methods=['POST'])
@token_required
@require_permission("reminder:create_own")
def create_reminder():
    data = request.json
    user_id = g.user_id
    reminder = ReminderRepository.create(
        user_id, data['medication_name'], data['dosage'], 
        data['time'], data['days']
    )
    return jsonify(reminder.to_dict()), 201

@reminders_bp.route('/<int:reminder_id>', methods=['DELETE'])
@token_required
@require_permission("reminder:delete_own")
def delete_reminder(reminder_id):
    user_id = g.user_id
    success = ReminderRepository.delete(reminder_id, user_id)
    if success:
        return jsonify({'message': 'Reminder deleted'}), 200
    return jsonify({'error': 'Reminder not found'}), 404

@reminders_bp.route('/<int:reminder_id>/toggle', methods=['POST'])
@token_required
@require_permission("reminder:toggle_own")
def toggle_reminder(reminder_id):
    user_id = g.user_id
    reminder = ReminderRepository.toggle(reminder_id, user_id)
    if reminder:
        return jsonify(reminder.to_dict()), 200
    return jsonify({'error': 'Reminder not found'}), 404
