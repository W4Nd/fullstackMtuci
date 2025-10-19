import axios from 'axios';
import type { Reminder, NewReminder } from '../types';

const API_BASE_URL = 'http://127.0.0.1:5000/api/v1';

export const apiService = {
  async getReminders(): Promise<Reminder[]> {
    const response = await axios.get<Reminder[]>(`${API_BASE_URL}/reminders`, {
      timeout: 5000,
    });
    return response.data;
  },

  async addReminder(reminderData: NewReminder): Promise<Reminder> {
    const response = await axios.post<Reminder>(`${API_BASE_URL}/reminders`, reminderData, {
      timeout: 5000,
    });
    return response.data;
  },

  async deleteReminder(id: number): Promise<void> {
    await axios.delete(`${API_BASE_URL}/reminders/${id}`, {
      timeout: 5000,
    });
  },

  async toggleReminder(id: number): Promise<void> {
    await axios.post(`${API_BASE_URL}/reminders/${id}/toggle`, {}, {
      timeout: 5000,
    });
  }
};