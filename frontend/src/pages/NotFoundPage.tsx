import React, { useEffect } from 'react';
import { Link } from 'react-router-dom';
import SEO from '../components/SEO'; 

const NotFoundPage: React.FC = () => {
  useEffect(() => {
    document.title = "404 — Страница не найдена | Medication Reminder";
  }, []);

  return (
    <>
      <SEO
        title="404"
        description="Страница не найдена. Вернитесь на главную."
        canonical="/404"
        noIndex={true}
      />
      
      <main 
        style={{ 
          minHeight: '100vh', 
          background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'center',
          padding: '2rem'
        }}
        role="main"
        aria-label="Страница ошибки 404"
      >
        <article style={{ 
          textAlign: 'center', 
          background: 'white',
          padding: '3rem 2rem',
          borderRadius: '1rem',
          boxShadow: '0 10px 25px rgba(0,0,0,0.1)',
          maxWidth: '500px',
          width: '100%'
        }}>
          <div style={{ fontSize: '6rem', marginBottom: '1rem' }} aria-hidden="true">😕</div>
          
          <h1 style={{ 
            fontSize: '3rem', 
            fontWeight: 'bold', 
            color: '#1f2937', 
            marginBottom: '1rem' 
          }}>
            404
          </h1>
          
          <p style={{ 
            fontSize: '1.25rem', 
            color: '#6b7280', 
            marginBottom: '2rem',
            lineHeight: '1.6'
          }}>
            Упс! Страница не найдена
          </p>
          
          <p style={{ 
            color: '#9ca3af', 
            marginBottom: '2.5rem' 
          }}>
            Возможно, вы ввели неправильный адрес или страница была перемещена
          </p>
          
          <Link 
            to="/"
            style={{
              display: 'inline-block',
              padding: '0.75rem 2rem',
              background: '#4f46e5',
              color: 'white',
              textDecoration: 'none',
              borderRadius: '0.5rem',
              fontWeight: '600',
              fontSize: '1rem',
              transition: 'all 0.2s'
            }}
            onMouseEnter={(e) => {
              e.currentTarget.style.background = '#4338ca';
              e.currentTarget.style.transform = 'translateY(-2px)';
            }}
            onMouseLeave={(e) => {
              e.currentTarget.style.background = '#4f46e5';
              e.currentTarget.style.transform = 'translateY(0)';
            }}
          >
            Вернуться на главную
          </Link>
        </article>
      </main>
    </>
  );
};

export default NotFoundPage;