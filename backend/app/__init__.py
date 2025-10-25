from flask import Flask, jsonify
import os
from dotenv import load_dotenv
from flask_cors import CORS
import logging
from logging.handlers import RotatingFileHandler
import sys
import atexit
import signal

load_dotenv()

def create_app():
    app = Flask(__name__)
    
    # Сначала создаем папки
    if not os.path.exists('data'):
        os.makedirs('data')
    if not os.path.exists('logs'):
        os.makedirs('logs')
    
    # Настройка логирования
    setup_logging(app)
    
    CORS(app, 
         origins=["http://localhost:5173", "http://127.0.0.1:5173"],
         methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
         allow_headers=["Content-Type", "Authorization"])
    
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')
    
    # Регистрация API blueprint
    from app.api import bp as api_bp
    app.register_blueprint(api_bp, url_prefix='/api/v1')
    
    from app.api.auth import bp as auth_bp
    app.register_blueprint(auth_bp, url_prefix='/api/v1')
    
    # Регистрация обработчиков ошибок
    from app.errors.handlers import register_error_handlers
    register_error_handlers(app)
    
    # Запуск службы уведомлений
    from app.services.notification_service import NotificationService
    notification_service = NotificationService()
    notification_service.start_scheduler()
    
    def shutdown_handler(signal_num=None, frame=None):
        """Обработчик завершения работы"""
        print('\n🔴 Остановка приложения...')
        notification_service.stop_scheduler()
        print('✅ Приложение корректно остановлено')
        sys.exit(0)
        
    signal.signal(signal.SIGINT, shutdown_handler)   # Ctrl+C
    signal.signal(signal.SIGTERM, shutdown_handler)  # Сигнал завершения
    
    # Регистрируем обработчик для atexit (на всякий случай)
    atexit.register(shutdown_handler)
    
    return app
    
    # Health check
    @app.route('/health')
    def health_check():
        return jsonify({
            'status': 'healthy',
            'timestamp': __import__('datetime').datetime.now().isoformat(),
            'version': '1.0.0'
        })
    
    app.logger.info('Medication Reminder application started successfully')
    return app

def setup_logging(app):
    """Настройка логирования"""
    try:
        file_handler = RotatingFileHandler(
            'logs/medication_reminder.log', 
            maxBytes=10240, 
            backupCount=10
        )
        file_handler.setFormatter(logging.Formatter(
            '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'
        ))
        file_handler.setLevel(logging.INFO)
        app.logger.addHandler(file_handler)
        app.logger.setLevel(logging.INFO)
    except Exception as e:
        # Fallback на консольное логирование
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)
        app.logger.addHandler(console_handler)
        app.logger.setLevel(logging.INFO)