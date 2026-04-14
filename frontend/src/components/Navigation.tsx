import React from 'react';
import { Link } from 'react-router-dom';
import { useAuth } from '../contexts/AuthContext';

const Navigation: React.FC = () => {
  const { user, logout, roles } = useAuth();

  return (
    <nav style={{
      background: 'rgba(255, 255, 255, 0.95)',
      padding: '1rem 2rem',
      boxShadow: '0 2px 10px rgba(0,0,0,0.1)',
      backdropFilter: 'blur(10px)'
    }}>
      <div style={{
        display: 'flex',
        justifyContent: 'space-between',
        alignItems: 'center',
        maxWidth: '1200px',
        margin: '0 auto'
      }}>
        <Link to="/" style={{
          textDecoration: 'none',
          fontSize: '1.5rem',
          fontWeight: 'bold',
          color: '#4f46e5'
        }}>
          💊 Medication Reminder
        </Link>

        <div style={{ display: 'flex', alignItems: 'center', gap: '1rem' }}>
            {user ? (
              <>
                <span style={{ color: '#6b7280' }}>
                  Привет, {user.username}!
                </span>
            
                <Link to="/profile" style={{
                  background: '#7b81fa',
                  color: 'white',
                  padding: '0.5rem 1rem',
                  borderRadius: '0.5rem',
                  textDecoration: 'none',
                  cursor: 'pointer'
                }}>
                  👤 Профиль
                </Link>
            
                {roles.includes('admin') && (
                  <Link to="/admin" style={{
                    background: '#10b981',
                    color: 'white',
                    padding: '0.5rem 1rem',
                    borderRadius: '0.5rem',
                    textDecoration: 'none',
                    cursor: 'pointer'
                  }}>
                    ⚙️ Админка
                  </Link>
                )}
            
                <button
                  onClick={logout}
                  style={{
                    background: '#ef4444',
                    color: 'white',
                    border: 'none',
                    padding: '0.5rem 1rem',
                    borderRadius: '0.5rem',
                    cursor: 'pointer'
                  }}
                >
                  Выйти
                </button>
              </>
            ) : (
            <Link to="/auth" style={{
              background: '#4f46e5',
              color: 'white',
              padding: '0.5rem 1rem',
              borderRadius: '0.5rem',
              textDecoration: 'none'
            }}>
              Войти
            </Link>
          )}
        </div>
      </div>
    </nav>
  );
};

export default Navigation;
