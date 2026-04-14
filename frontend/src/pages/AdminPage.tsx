import React, { useState, useEffect } from 'react';
import { useAuth } from '../contexts/AuthContext';
import { apiService } from '../services/api';
import SEO from '../components/SEO';


const AdminPage: React.FC = () => {
  const { hasPermission } = useAuth();
  const [users, setUsers] = useState<any[]>([]);
  const [loading, setLoading] = useState(false);

  const fetchAllUsers = async () => {
    if (!hasPermission('user:*')) return;
    
    try {
      setLoading(true);
      const data = await apiService.getAllUsers();  // ✅ Правильный метод!
      setUsers(data.users || []);
      console.log('✅ Users loaded:', data.users);
    } catch (error: any) {
      console.error('❌ Error:', error.response?.data?.error || error.message);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchAllUsers();
  }, []);

    return (
        <>
            <SEO
              title="Профиль"
              description="Личный кабинет пользователя"
              canonical="/profile"
              noIndex={true} 
            />
    <div style={{ padding: '2rem', maxWidth: '1200px', margin: '0 auto' }}>
      <h1 style={{ color: '#1f2937' }}>⚙️ Админ панель</h1>
      
      {hasPermission('user:*') && (
        <div style={{ 
          background: '#eff6ff', 
          padding: '1.5rem', 
          borderRadius: '8px',
          borderLeft: '4px solid #3b82f6',
          marginBottom: '1.5rem'
        }}>
          <div style={{ display: 'flex', gap: '1rem', alignItems: 'center', marginBottom: '1rem' }}>
            <h2 style={{ color: '#2563eb', margin: 0 }}>👥 Все пользователи</h2>
            <button 
              onClick={fetchAllUsers}
              disabled={loading}
              style={{
                background: '#3b82f6',
                color: 'white',
                padding: '0.5rem 1rem',
                borderRadius: '0.375rem',
                border: 'none',
                cursor: loading ? 'not-allowed' : 'pointer'
              }}
            >
              {loading ? '🔄 Загрузка...' : '🔄 Обновить'}
            </button>
          </div>
          
          {users.length > 0 ? (
            <div style={{ maxHeight: '400px', overflowY: 'auto' }}>
              {users.map((user: any) => (
                <div key={user.id} style={{
                  padding: '1rem',
                  border: '1px solid #e5e7eb',
                  borderRadius: '0.5rem',
                  marginBottom: '0.5rem',
                  background: 'white'
                }}>
                  <strong>ID: {user.id}</strong> | 
                  <span style={{ margin: '0 1rem' }}>👤 {user.username}</span> | 
                  <span style={{ color: '#6b7280' }}>📧 {user.email}</span>
                </div>
              ))}
            </div>
          ) : (
            <p style={{ color: '#6b7280' }}>👥 Пользователи не найдены</p>
          )}
        </div>
      )}
            </div>
        </>
  );
};

export default AdminPage;
