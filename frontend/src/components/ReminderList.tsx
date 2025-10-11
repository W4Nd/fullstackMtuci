import React from 'react';
import type { Reminder } from '../types';

interface ReminderListProps {
  reminders: Reminder[];
  onToggle: (id: number) => void;
  onDelete: (id: number) => void;
}

const ReminderList: React.FC<ReminderListProps> = ({ reminders, onToggle, onDelete }) => {
  const dayNames = ['Пн', 'Вт', 'Ср', 'Чт', 'Пт', 'Сб', 'Вс'];

  if (reminders.length === 0) {
    return (
      <div style={{ background: 'white', borderRadius: '8px', padding: '1.5rem', textAlign: 'center', boxShadow: '0 2px 5px rgba(0,0,0,0.1)' }}>
        <p style={{ color: '#6b7280' }}>Нет добавленных напоминаний</p>
      </div>
    );
  }

  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: '1rem' }}>
      <h2 style={{ fontSize: '1.5rem', fontWeight: 'bold', marginBottom: '1rem' }}>Мои напоминания</h2>
      {reminders.map(reminder => (
        <div
          key={reminder.id}
          style={{
            background: 'white',
            borderRadius: '8px',
            padding: '1.5rem',
            borderLeft: `4px solid ${reminder.is_active ? '#10b981' : '#d1d5db'}`,
            opacity: reminder.is_active ? 1 : 0.6,
            boxShadow: '0 2px 5px rgba(0,0,0,0.1)'
          }}
        >
          <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start' }}>
            <div style={{ flex: 1 }}>
              <h3 style={{ fontSize: '1.25rem', fontWeight: '600', color: '#1f2937' }}>
                {reminder.medication.name}
              </h3>
              <p style={{ color: '#6b7280', fontStyle: 'italic', marginTop: '0.25rem' }}>
                {reminder.medication.dosage}
              </p>
              <div style={{ display: 'flex', alignItems: 'center', marginTop: '0.5rem', color: '#374151' }}>
                <span style={{ fontSize: '1.125rem' }}>⏰</span>
                <span style={{ marginLeft: '0.5rem', fontWeight: '500' }}>{reminder.time}</span>
              </div>
              <div style={{ display: 'flex', flexWrap: 'wrap', gap: '0.25rem', marginTop: '0.75rem' }}>
                {reminder.days.map(day => (
                  <span
                    key={day}
                    style={{
                      background: '#dbeafe',
                      color: '#1e40af',
                      padding: '0.125rem 0.5rem',
                      borderRadius: '9999px',
                      fontSize: '0.75rem',
                      fontWeight: '500'
                    }}
                  >
                    {dayNames[day]}
                  </span>
                ))}
              </div>
            </div>
            <div style={{ display: 'flex', gap: '0.5rem', marginLeft: '1rem' }}>
              <button
                onClick={() => onToggle(reminder.id)}
                style={{
                  background: reminder.is_active ? '#fef3c7' : '#dcfce7',
                  color: reminder.is_active ? '#92400e' : '#166534',
                  padding: '0.25rem 0.75rem',
                  borderRadius: '0.25rem',
                  fontSize: '0.875rem',
                  fontWeight: '500',
                  border: 'none',
                  cursor: 'pointer'
                }}
              >
                {reminder.is_active ? 'Выключить' : 'Включить'}
              </button>
              <button
                onClick={() => onDelete(reminder.id)}
                style={{
                  background: '#fee2e2',
                  color: '#991b1b',
                  padding: '0.25rem 0.75rem',
                  borderRadius: '0.25rem',
                  fontSize: '0.875rem',
                  fontWeight: '500',
                  border: 'none',
                  cursor: 'pointer'
                }}
              >
                Удалить
              </button>
            </div>
          </div>
        </div>
      ))}
    </div>
  );
};

export default ReminderList;