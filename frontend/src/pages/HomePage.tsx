import React, { useState, useEffect } from 'react';
import type { Reminder, NewReminder } from '../types';
import { apiService } from '../services/api';
import ReminderForm from '../components/ReminderForm';
import ReminderList from '../components/ReminderList';

const HomePage: React.FC = () => {
  const [reminders, setReminders] = useState<Reminder[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    console.log('HomePage component mounted, loading reminders...');
    loadReminders();
  }, []);

  const loadReminders = async () => {
    try {
      setLoading(true);
      setError(null);
      console.log('Making API request to load reminders...');
      
      const data = await apiService.getReminders();
      console.log('Reminders loaded successfully:', data);
      
      setReminders(data);
    } catch (err) {
      const errorMessage = `Ошибка при загрузке напоминаний: ${err}`;
      console.error('Error loading reminders:', err);
      setError(errorMessage);
    } finally {
      setLoading(false);
    }
  };

  const handleAddReminder = async (newReminder: NewReminder) => {
    try {
      setError(null);
      console.log('Adding new reminder:', newReminder);
      
      const addedReminder = await apiService.addReminder(newReminder);
      console.log('Reminder added successfully:', addedReminder);
      
      setReminders(prev => [...prev, addedReminder]);
    } catch (err) {
      const errorMessage = `Ошибка при добавлении напоминания: ${err}`;
      console.error('Error adding reminder:', err);
      setError(errorMessage);
    }
  };

  const handleToggleReminder = async (id: number) => {
    try {
      setError(null);
      console.log('Toggling reminder with ID:', id);
      
      await apiService.toggleReminder(id);
      setReminders(prev =>
        prev.map(reminder =>
          reminder.id === id
            ? { ...reminder, is_active: !reminder.is_active }
            : reminder
        )
      );
      
      console.log('Reminder toggled successfully');
    } catch (err) {
      const errorMessage = `Ошибка при изменении статуса напоминания: ${err}`;
      console.error('Error toggling reminder:', err);
      setError(errorMessage);
    }
  };

  const handleDeleteReminder = async (id: number) => {
    if (window.confirm('Вы уверены, что хотите удалить это напоминание?')) {
      try {
        setError(null);
        console.log('Deleting reminder with ID:', id);
        
        await apiService.deleteReminder(id);
        setReminders(prev => prev.filter(reminder => reminder.id !== id));
        
        console.log('Reminder deleted successfully');
      } catch (err) {
        const errorMessage = `Ошибка при удалении напоминания: ${err}`;
        console.error('Error deleting reminder:', err);
        setError(errorMessage);
      }
    }
  };

  console.log('Rendering HomePage component. Loading:', loading, 'Reminders count:', reminders.length);

  return (
    <div style={{ minHeight: '100vh', background: '#f9fafb' }}>
      <div style={{ maxWidth: '56rem', margin: '0 auto', padding: '2rem 1rem' }}>
        {/* Заголовок */}
        <header style={{ textAlign: 'center', marginBottom: '2rem' }}>
          <h1 style={{ fontSize: '2.25rem', fontWeight: 'bold', color: '#1f2937', marginBottom: '0.5rem' }}>
            💊 Напоминания о лекарствах
          </h1>
          <p style={{ color: '#6b7280' }}>
            Никогда не забывайте принимать лекарства вовремя
          </p>
        </header>

        {/* Сообщения об ошибках */}
        {error && (
          <div style={{ 
            background: '#fecaca', 
            border: '1px solid #f87171', 
            color: '#b91c1c', 
            padding: '0.75rem 1rem', 
            borderRadius: '0.375rem', 
            marginBottom: '1.5rem' 
          }}>
            {error}
            <button 
              onClick={() => setError(null)}
              style={{ 
                marginLeft: '10px', 
                background: 'none', 
                border: 'none', 
                color: '#b91c1c', 
                cursor: 'pointer' 
              }}
            >
              ✕
            </button>
          </div>
        )}

        {/* Форма добавления */}
        <ReminderForm onSubmit={handleAddReminder} />

        {/* Список напоминаний */}
        {loading ? (
          <div style={{ textAlign: 'center', padding: '2rem 0' }}>
            <div style={{ 
              animation: 'spin 1s linear infinite', 
              border: '2px solid #2563eb', 
              borderTop: '2px solid transparent',
              borderRadius: '50%', 
              width: '3rem', 
              height: '3rem', 
              margin: '0 auto' 
            }}></div>
            <p style={{ marginTop: '0.5rem', color: '#6b7280' }}>Загрузка напоминаний...</p>
          </div>
        ) : (
          <ReminderList
            reminders={reminders}
            onToggle={handleToggleReminder}
            onDelete={handleDeleteReminder}
          />
        )}

        {/* Отладочная информация */}
        <div style={{ 
          marginTop: '2rem', 
          padding: '1rem', 
          background: '#f3f4f6', 
          borderRadius: '0.5rem',
          fontSize: '0.875rem',
          color: '#6b7280'
        }}>
          <strong>Отладка:</strong> Загружено {reminders.length} напоминаний
        </div>
      </div>
    </div>
  );
};

export default HomePage;