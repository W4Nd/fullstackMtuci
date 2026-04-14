import React from 'react';
import { Navigate } from 'react-router-dom';
import { useAuth } from '../contexts/AuthContext';

interface RoleProtectedRouteProps {
  children: React.ReactNode;
  requiredPermission?: string;
  requiredRole?: string;
}

const RoleProtectedRoute: React.FC<RoleProtectedRouteProps> = ({ 
  children, 
  requiredPermission, 
  requiredRole 
}) => {
  const { user, roles, loading, hasPermission } = useAuth();

  if (loading) {
    return <div>Загрузка...</div>;
  }

  if (!user) {
    return <Navigate to="/auth" replace />;
  }

  if (requiredRole && !roles.includes(requiredRole)) {
    return <Navigate to="/" replace />;
  }

  if (requiredPermission && !hasPermission(requiredPermission)) {
    return <div>Нет доступа</div>;
  }

  return <>{children}</>;
};

export default RoleProtectedRoute;
