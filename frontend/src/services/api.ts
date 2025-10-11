import axios from 'axios';
import type { Reminder, NewReminder } from '../types';

const API_BASE_URL = 'http://localhost:5000/api';

export const apiService = {
  async getReminders(): Promise<Reminder[]> {
    const response = await axios.get<Reminder[]>(`${API_BASE_URL}/reminders`);
    return response.data;
  },

  async addReminder(reminderData: NewReminder): Promise<Reminder> {
    const response = await axios.post<Reminder>(`${API_BASE_URL}/reminders`, reminderData);
    return response.data;
  },

  async deleteReminder(id: number): Promise<void> {
    await axios.delete(`${API_BASE_URL}/reminders/${id}`);
  },

  async toggleReminder(id: number): Promise<void> {
    await axios.post(`${API_BASE_URL}/reminders/${id}/toggle`);
  }
};