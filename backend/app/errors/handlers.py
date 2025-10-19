from flask import jsonify
import logging

logger = logging.getLogger(__name__)

def register_error_handlers(app):
    """Регистрация обработчиков ошибок"""
    
    @app.errorhandler(400)
    def bad_request_error(error):
        logger.warning(f'Bad request: {str(error)}')
        return jsonify({'error': 'Неверный запрос', 'message': str(error)}), 400
    
    @app.errorhandler(404)
    def not_found_error(error):
        logger.warning(f'Resource not found: {str(error)}')
        return jsonify({'error': 'Ресурс не найден'}), 404
    
    @app.errorhandler(405)
    def method_not_allowed_error(error):
        logger.warning(f'Method not allowed: {str(error)}')
        return jsonify({'error': 'Метод не разрешен'}), 405
    
    @app.errorhandler(500)
    def internal_error(error):
        logger.error(f'Internal server error: {str(error)}')
        return jsonify({'error': 'Внутренняя ошибка сервера'}), 500
    
    @app.errorhandler(Exception)
    def handle_unexpected_error(error):
        logger.error(f'Unexpected error: {str(error)}')
        return jsonify({'error': 'Непредвиденная ошибка'}), 500