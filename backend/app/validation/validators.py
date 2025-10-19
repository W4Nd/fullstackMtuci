import re
from datetime import datetime

def validate_reminder_data(data):
    """Валидация данных для создания напоминания"""
    errors = []
    
    # Проверка названия лекарства
    medication_name = data.get('medication_name', '').strip()
    if not medication_name:
        errors.append("Название лекарства обязательно")
    elif len(medication_name) < 2:
        errors.append("Название лекарства должно содержать минимум 2 символа")
    elif len(medication_name) > 100:
        errors.append("Название лекарства не должно превышать 100 символов")
    
    # Проверка дозировки
    dosage = data.get('dosage', '').strip()
    if not dosage:
        errors.append("Дозировка обязательна")
    elif len(dosage) > 50:
        errors.append("Дозировка не должна превышать 50 символов")
    
    # Проверка времени
    time_str = data.get('time', '')
    if not time_str:
        errors.append("Время приема обязательно")
    else:
        try:
            datetime.strptime(time_str, "%H:%M")
        except ValueError:
            errors.append("Неверный формат времени. Используйте HH:MM")
    
    # Проверка дней недели
    days = data.get('days', [])
    if not days:
        errors.append("Необходимо выбрать хотя бы один день недели")
    elif not isinstance(days, list):
        errors.append("Дни недели должны быть списком")
    else:
        for day in days:
            if not isinstance(day, int) or day < 0 or day > 6:
                errors.append("Дни недели должны быть числами от 0 до 6")
                break
    
    return errors