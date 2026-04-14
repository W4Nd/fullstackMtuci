import axios, { AxiosError } from 'axios';
import type { AxiosRequestConfig } from 'axios';
import type { Reminder, NewReminder, User } from '../types';

const API_BASE_URL = 'http://127.0.0.1:8000/api/v1';  // FastAPI порт

const apiClient = axios.create({
  baseURL: API_BASE_URL,
  timeout: 10000,
});

// 🔥 Тип для retry
interface RetryableRequestConfig extends AxiosRequestConfig {
  _retry?: boolean;
}

let isRefreshing = false;
let failedQueue: Array<{resolve: (value?: any) => void; reject: (reason?: any) => void}> = [];

const processQueue = (error: AxiosError | null, token: string | null = null) => {
  failedQueue.forEach(prom => {
    if (error) prom.reject(error);
    else prom.resolve(token);
  });
  failedQueue = [];
};

// 🔥 REQUEST INTERCEPTOR (добавляет access_token)
apiClient.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('auth_access_token');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  }
);

// 🔥 RESPONSE INTERCEPTOR (5.3 автообновление токена)
apiClient.interceptors.response.use(
  (response) => response,
  async (error: AxiosError) => {
    const originalRequest = error.config as RetryableRequestConfig;
    
    if (error.response?.status === 401 && !originalRequest?._retry) {
      if (isRefreshing) {
        return new Promise((resolve, reject) => {
          failedQueue.push({ resolve, reject });
        }).then((token) => {
          originalRequest!.headers!.Authorization = `Bearer ${token}`;
          return apiClient(originalRequest!);
        }).catch(err => Promise.reject(err));
      }

      originalRequest!._retry = true;
      isRefreshing = true;

      try {
        const refreshToken = localStorage.getItem('auth_refresh_token');
        if (!refreshToken) throw new Error('No refresh token');

        const response = await axios.post(`${API_BASE_URL}/auth/refresh`, {}, {
          headers: { Authorization: `Bearer ${refreshToken}` }
        });
        
        const { access_token, refresh_token } = response.data;
        localStorage.setItem('auth_access_token', access_token);
        localStorage.setItem('auth_refresh_token', refresh_token);
        
        processQueue(null, access_token);
        originalRequest!.headers!.Authorization = `Bearer ${access_token}`;
        return apiClient(originalRequest!);
        
      } catch (refreshError) {
        processQueue(refreshError as AxiosError, null);
        localStorage.clear();
        window.dispatchEvent(new Event('authChange'));
        window.location.href = '/auth';
        return Promise.reject(refreshError);
      } finally {
        isRefreshing = false;
      }
    }
    return Promise.reject(error);
  }
);

export const apiService = {
  // 🔥 LOGIN (OAuth2PasswordRequestForm)
  async login(credentials: { username: string; password: string }): Promise<any> {
    const params = new URLSearchParams();
    params.append('username', credentials.username);
    params.append('password', credentials.password);
    
    const response = await apiClient.post('/auth/token', params);
    const { access_token, refresh_token } = response.data;
    
    localStorage.setItem('auth_access_token', access_token);
    localStorage.setItem('auth_refresh_token', refresh_token);
    localStorage.setItem('user_roles', JSON.stringify(response.data.roles || ['user']));
    
    window.dispatchEvent(new Event('authChange'));
    return response.data;
  },

  // 🔥 LOGOUT
  async logout(): Promise<void> {
    const refreshToken = localStorage.getItem('auth_refresh_token');
    try {
      await axios.post(`${API_BASE_URL}/auth/logout`, {}, {
        headers: { Authorization: `Bearer ${refreshToken}` }
      });
    } catch(e) {
      console.log('Logout request failed');
    }
    localStorage.clear();
    window.dispatchEvent(new Event('authChange'));
  },

  // 🔥 Текущий пользователь
  async getMe(): Promise<{ user: User; roles: string[] }> {
    const response = await apiClient.get('/auth/me');
    return response.data;
  },

  // Напоминания
  async getReminders(): Promise<Reminder[]> {
    const response = await apiClient.get<Reminder[]>('/reminders');
    return response.data;
  },

  async addReminder(reminderData: NewReminder): Promise<Reminder> {
    const response = await apiClient.post<Reminder>('/reminders', reminderData);
    return response.data;
  },

  async deleteReminder(id: number): Promise<void> {
    await apiClient.delete(`/reminders/${id}`);
  },

  async toggleReminder(id: number): Promise<Reminder> {
    const response = await apiClient.post<Reminder>(`/reminders/${id}/toggle`);
    return response.data;
  },

  // Профиль
  async getProfile(): Promise<any> {
    const response = await apiClient.get('/profile/me');
    return response.data;
  },

  async updateProfile(data: any): Promise<any> {
    const response = await apiClient.put('/profile/me', data);
    return response.data;
  },

  // Admin
  async getAllUsers(): Promise<{ users: User[]; count: number }> {
    const response = await apiClient.get('/admin/users');
    return response.data;
    },
  
    async register(registerData: { username: string; email: string; password: string }): Promise<any> {
      const response = await apiClient.post('/auth/register', registerData);
      // Возвращаем для совместимости со старым кодом
      return {
        token: response.data.access_token,
        refresh_token: response.data.refresh_token,
        user: response.data.user,
        roles: response.data.roles || ['user']
      };
    },
};

