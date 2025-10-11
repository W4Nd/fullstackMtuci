import React, { useState } from 'react';
import type { NewReminder } from '../types';

interface ReminderFormProps {
  onSubmit: (reminder: NewReminder) => void;
}

const ReminderForm: React.FC<ReminderFormProps> = ({ onSubmit }) => {
  const [formData, setFormData] = useState<NewReminder>({
    medication_name: '',
    dosage: '',
    time: '',
    days: []
  });

  const dayNames = ['Пн', 'Вт', 'Ср', 'Чт', 'Пт', 'Сб', 'Вс'];

  const handleDayToggle = (dayIndex: number) => {
    setFormData(prev => ({
      ...prev,
      days: prev.days.includes(dayIndex)
        ? prev.days.filter(d => d !== dayIndex)
        : [...prev.days, dayIndex]
    }));
  };

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (formData.medication_name && formData.dosage && formData.time && formData.days.length > 0) {
      onSubmit(formData);
      setFormData({
        medication_name: '',
        dosage: '',
        time: '',
        days: []
      });
    } else {
      alert('Пожалуйста, заполните все поля');
    }
  };

  return (
    <div style={{ background: 'white', borderRadius: '8px', padding: '1.5rem', marginBottom: '1.5rem', boxShadow: '0 2px 5px rgba(0,0,0,0.1)' }}>
      <h2 style={{ fontSize: '1.5rem', fontWeight: 'bold', marginBottom: '1rem' }}>Добавить новое напоминание</h2>
      <form onSubmit={handleSubmit} style={{ display: 'flex', flexDirection: 'column', gap: '1rem' }}>
        <div>
          <label style={{ display: 'block', fontSize: '0.875rem', fontWeight: '500', color: '#374151', marginBottom: '0.5rem' }}>
            Название лекарства
          </label>
          <input
            type="text"
            value={formData.medication_name}
            onChange={(e) => setFormData(prev => ({ ...prev, medication_name: e.target.value }))}
            style={{ width: '100%', padding: '0.5rem 0.75rem', border: '1px solid #d1d5db', borderRadius: '0.375rem' }}
            required
          />
        </div>

        <div>
          <label style={{ display: 'block', fontSize: '0.875rem', fontWeight: '500', color: '#374151', marginBottom: '0.5rem' }}>
            Дозировка
          </label>
          <input
            type="text"
            value={formData.dosage}
            onChange={(e) => setFormData(prev => ({ ...prev, dosage: e.target.value }))}
            style={{ width: '100%', padding: '0.5rem 0.75rem', border: '1px solid #d1d5db', borderRadius: '0.375rem' }}
            required
          />
        </div>

        <div>
          <label style={{ display: 'block', fontSize: '0.875rem', fontWeight: '500', color: '#374151', marginBottom: '0.5rem' }}>
            Время приема
          </label>
          <input
            type="time"
            value={formData.time}
            onChange={(e) => setFormData(prev => ({ ...prev, time: e.target.value }))}
            style={{ padding: '0.5rem 0.75rem', border: '1px solid #d1d5db', borderRadius: '0.375rem' }}
            required
          />
        </div>

        <div>
          <label style={{ display: 'block', fontSize: '0.875rem', fontWeight: '500', color: '#374151', marginBottom: '0.5rem' }}>
            Дни недели
          </label>
          <div style={{ display: 'flex', flexWrap: 'wrap', gap: '0.75rem' }}>
            {dayNames.map((day, index) => (
              <label key={index} style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
                <input
                  type="checkbox"
                  checked={formData.days.includes(index)}
                  onChange={() => handleDayToggle(index)}
                  style={{ width: '1rem', height: '1rem' }}
                />
                <span style={{ fontSize: '0.875rem' }}>{day}</span>
              </label>
            ))}
          </div>
        </div>

        <button
          type="submit"
          style={{ background: '#2563eb', color: 'white', padding: '0.5rem 1.5rem', border: 'none', borderRadius: '0.375rem', cursor: 'pointer' }}
        >
          Добавить напоминание
        </button>
      </form>
    </div>
  );
};

export default ReminderForm;