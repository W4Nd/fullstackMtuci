from flask import Blueprint, render_template, request, jsonify, redirect, url_for
from app.storage import load_reminders, save_reminders, get_next_id
from app.models import Reminder, Medication

bp = Blueprint('main', __name__)

@bp.route('/')
def index():
    return render_template('index.html')

@bp.route('/reminders')
def reminders():
    reminders_list = load_reminders()
    return render_template('reminders.html', reminders=reminders_list)

@bp.route('/api/reminders', methods=['GET'])
def get_reminders():
    reminders_list = load_reminders()
    return jsonify([reminder.to_dict() for reminder in reminders_list])

@bp.route('/api/reminders', methods=['POST'])
def add_reminder():
    data = request.json
    reminders_list = load_reminders()
    
    new_reminder = Reminder(
        id=get_next_id(reminders_list),
        medication=Medication(
            name=data['medication_name'],
            dosage=data['dosage']
        ),
        time=data['time'],
        days=data.get('days', []),
        is_active=True
    )
    
    reminders_list.append(new_reminder)
    save_reminders(reminders_list)
    
    return jsonify(new_reminder.to_dict()), 201

@bp.route('/api/reminders/<int:reminder_id>', methods=['DELETE'])
def delete_reminder(reminder_id):
    reminders_list = load_reminders()
    reminders_list = [r for r in reminders_list if r.id != reminder_id]
    save_reminders(reminders_list)
    
    return jsonify({'message': 'Reminder deleted'}), 200

@bp.route('/api/reminders/<int:reminder_id>/toggle', methods=['POST'])
def toggle_reminder(reminder_id):
    reminders_list = load_reminders()
    for reminder in reminders_list:
        if reminder.id == reminder_id:
            reminder.is_active = not reminder.is_active
            break
    
    save_reminders(reminders_list)
    return jsonify({'message': 'Reminder toggled'}), 200