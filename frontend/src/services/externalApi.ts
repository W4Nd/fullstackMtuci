import axios from 'axios';

const externalApi = axios.create({
  baseURL: '/api/v1/external',
  timeout: 15000, // 15 секунд
});

// Interceptor для graceful degradation
externalApi.interceptors.response.use(
  response => response,
  error => {
    if (error.code === 'ECONNABORTED' || error.message?.includes('timeout')) {
      console.warn('External API timeout, using fallback');
      return Promise.resolve({ fallback: true, message: 'Данные временно недоступны' });
    }
    return Promise.reject(error);
  }
);

export const ExternalAPI = {
  searchDrug: (drugName: string, limit = 5) => 
    externalApi.get(`/fda/drug/search?drug_name=${encodeURIComponent(drugName)}&limit=${limit}`)
};