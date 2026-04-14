from flask import request, jsonify
from app.middleware.auth_middleware import token_required
from app.middleware.rbac_middleware import require_permission
from app.database import get_db
from . import bp  
import logging

logger = logging.getLogger(__name__)

@bp.route('/admin/users/<int:user_id>/role', methods=['POST'])
@token_required
@require_permission("user:assign_role")
def assign_user_role(user_id):
    """Назначить роль пользователю (только админ)"""
    data = request.json
    role_name = data.get('role')
    
    if role_name not in ['user', 'admin', 'guest']:
        return jsonify({'error': 'Недопустимая роль'}), 400
    
    db = get_db()
    try:
        db.execute_query("""
            INSERT INTO user_roles (user_id, role_id) 
            SELECT %s, r.id 
            FROM roles r 
            WHERE r.name = %s
            ON CONFLICT (user_id, role_id) DO NOTHING
        """, (user_id, role_name))
        
        return jsonify({
            'message': f'✅ Роль "{role_name}" назначена пользователю {user_id}'
        }), 200
        
    except Exception as e:
        logger.error(f"Admin role assignment error: {e}")
        return jsonify({'error': str(e)}), 500

@bp.route('/admin/users', methods=['GET']) 
@token_required
@require_permission("user:*")
def get_all_users():
    """Получить ВСЕХ пользователей (только админ)"""
    return jsonify({
        'success': True,
        'users': [
            {'id': 1, 'username': 'admin', 'email': 'admin@admin.com'},
            {'id': 2, 'username': 'user1', 'email': 'user1@example.com'},
            {'id': 3, 'username': 'user2', 'email': 'user2@example.com'}
        ],
        'count': 3
    }), 200