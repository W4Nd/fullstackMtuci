import sys
import os

# Добавляем текущую директорию в путь
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

print("=== DEBUG IMPORTS ===")

modules_to_check = [
    'app',
    'app.api',
    'app.api.reminders', 
    'app.repositories.reminder_repository',
    'app.models',
    'app.storage',
    'app.validation.validators',
    'app.errors.handlers',
    'app.services.notification_service'
]

for module_path in modules_to_check:
    try:
        __import__(module_path)
        print(f"✅ {module_path}")
    except ImportError as e:
        print(f"❌ {module_path}: {e}")