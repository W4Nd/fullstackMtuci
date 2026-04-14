from ..middleware.rbac_middleware import require_permission
from flask import Blueprint, request, jsonify, g
from app.middleware.auth_middleware import token_required
from app.services.profile_service import ProfileService
from app.repositories.user_repository import UserRepository
from app.database import get_db
import logging

logger = logging.getLogger(__name__)

profile_bp = Blueprint('profile', __name__)

@profile_bp.route('/profile/me', methods=['GET'])
@token_required
@require_permission('user:read_own')
def get_my_profile():
    """Получить мой профиль"""
    try:
        user_id = g.user_id
        print(f"\n{'='*50}")
        print(f"🔍 GET /profile/me called")
        print(f"👤 User ID: {user_id}")
        print(f"👤 Username: {g.username}")
        
        print(f"📦 Getting DB connection...")
        db = get_db()
        print(f"✅ DB connection: {db}")
        
        print(f"📦 Creating UserRepository...")
        user_repo = UserRepository(db)
        print(f"✅ UserRepository created")
        
        print(f"📦 Creating ProfileService...")
        profile_service = ProfileService(user_repo)
        print(f"✅ ProfileService created")
        
        print(f"📦 Fetching profile for user_id={user_id}...")
        profile = profile_service.get_profile(user_id)
        print(f"✅ Profile fetched: {profile}")
        
        if not profile:
            print(f"❌ Profile is None!")
            return jsonify({'error': 'Profile not found'}), 404
        
        print(f"✅ Returning profile")
        print(f"{'='*50}\n")
        return jsonify(profile), 200
        
    except Exception as e:
        print(f"❌ ERROR: {str(e)}")
        print(f"❌ Exception type: {type(e)}")
        import traceback
        traceback.print_exc()
        logger.error(f"ERROR in get_my_profile: {str(e)}", exc_info=True)
        return jsonify({'error': str(e)}), 500
    
@profile_bp.route('/profile/me', methods=['PUT'])
@token_required
@require_permission("user:update_own") 
def update_my_profile():
    """Обновить мой профиль"""
    try:
        user_id = g.user_id
        print(f"\n{'='*50}")
        print(f"🔍 PUT /profile/me called")
        print(f"👤 User ID: {user_id}")
        print(f"👤 Username: {g.username}")
        
        data = request.get_json()
        print(f"📦 Request data: {data}")
        
        if not data:
            print(f"❌ No data provided")
            return jsonify({'error': 'No data provided'}), 400
        
        print(f"📦 Getting DB connection...")
        db = get_db()
        print(f"✅ DB connection: {db}")
        
        print(f"📦 Creating UserRepository...")
        user_repo = UserRepository(db)
        print(f"✅ UserRepository created")
        
        print(f"📦 Creating ProfileService...")
        profile_service = ProfileService(user_repo)
        print(f"✅ ProfileService created")
        
        print(f"📦 Updating profile for user_id={user_id}...")
        result = profile_service.update_profile(user_id, data)
        print(f"✅ Update result: {result}")
        
        if result['success']:
            print(f"✅ Profile updated successfully")
            print(f"{'='*50}\n")
            return jsonify(result), 200
        else:
            print(f"❌ Update failed: {result['errors']}")
            print(f"{'='*50}\n")
            return jsonify(result), 400
            
    except Exception as e:
        print(f"❌ ERROR: {str(e)}")
        print(f"❌ Exception type: {type(e)}")
        import traceback
        traceback.print_exc()
        logger.error(f"ERROR in update_my_profile: {str(e)}", exc_info=True)
        return jsonify({'error': str(e)}), 500

