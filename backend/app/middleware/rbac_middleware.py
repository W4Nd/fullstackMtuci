from functools import wraps
from flask import jsonify, g
from app.services.rbac_service import RBACService
from app.database import get_db
from app.repositories.user_repository import UserRepository 

def require_permission(permission: str, check_owner: bool = True):
    """Декоратор проверки прав доступа."""
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            user_id = getattr(g, "user_id", None)
            if not user_id:
                return jsonify({"error": "Токен невалиден"}), 401

            roles = RBACService.get_user_roles(user_id)

            resource_owner_id = None
            if check_owner:
                if "user_id" in kwargs:
                    resource_owner_id = int(kwargs["user_id"])
                else:
                    resource_owner_id = user_id

            has_access = RBACService.has_permission(
                roles,
                permission,
                resource_owner_id=resource_owner_id,
            )

            if not has_access:
                return (
                    jsonify({"error": f"Недостаточно прав для действия: {permission}"}),
                    403,
                )

            return f(*args, **kwargs)

        return decorated_function
    return decorator
