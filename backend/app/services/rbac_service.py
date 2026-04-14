from typing import List
from app.database import get_db

RBAC_MATRIX = {
    "guest": ["auth:register", "auth:login", "auth:verify"],
    "user": [
        "user:read_own", "user:update_own",
        "reminder:read_own", "reminder:create_own", 
        "reminder:update_own", "reminder:delete_own", "reminder:toggle_own"
    ],
    "admin": ["user:*", "reminder:*", "role:*", "user:assign_role"]
}

class RBACService:
    @staticmethod
    def get_user_roles(user_id: int) -> List[str]:
        """Получить роли пользователя из БД"""
        db = get_db()
        result = db.execute_query("""
            SELECT r.name FROM user_roles ur 
            JOIN roles r ON ur.role_id = r.id 
            WHERE ur.user_id = %s
        """, (user_id,))
        return [row["name"] for row in result]
    
    @staticmethod
    def get_all_permissions(roles: List[str]) -> List[str]:
        """Получить все разрешения по ролям"""
        permissions = set()
        for role in roles:
            if role in RBAC_MATRIX:
                permissions.update(RBAC_MATRIX[role])
        return list(permissions)
    
    @staticmethod
    def has_permission(roles: List[str], permission: str, resource_owner_id: int = None) -> bool:
        """Проверка разрешения"""
        user_permissions = RBACService.get_all_permissions(roles)
        
        # Wildcard permissions
        for user_perm in user_permissions:
            if user_perm.endswith(":*") and ":" in permission:
                if user_perm.split(":")[0] == permission.split(":")[0]:
                    return True
        
        # Owner permissions (_own)
        if resource_owner_id and "_own" in permission:
            if str(resource_owner_id) == str(resource_owner_id):  # always true for own
                base_perm = permission.replace("_own", "")
                if base_perm in user_permissions:
                    return True
        
        return permission in user_permissions
