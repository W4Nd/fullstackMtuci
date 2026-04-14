// frontend/tests/mocks/server.ts
import { setupServer } from 'msw/node'
import { http, HttpResponse } from 'msw'

export const handlers = [
  // ✅ Успешный логин
  http.post('/api/v1/auth/token', async ({ request }) => {
    const formData = await request.formData()
    const username = formData.get('username')
    
    if (username === 'testuser' && formData.get('password') === 'correctpass') {
      return HttpResponse.json({
        access_token: 'mock_access_token_123',
        refresh_token: 'mock_refresh_token_456',
        user: { id: 1, username: 'testuser', email: 'test@example.com' },
        roles: ['user']
      }, { status: 200 })
    }
    
    return HttpResponse.json({ detail: 'Неверные данные' }, { status: 401 })
  }),

  // ✅ Получение профиля (требует токен)
  http.get('/api/v1/auth/me', ({ request }) => {
    const auth = request.headers.get('Authorization')
    if (auth === 'Bearer mock_access_token_123') {
      return HttpResponse.json({
        user: { id: 1, username: 'testuser', email: 'test@example.com' },
        roles: ['user']
      })
    }
    return HttpResponse.json({ detail: 'Не авторизован' }, { status: 401 })
  }),

  // ✅ Логаут
  http.post('/api/v1/auth/logout', () => {
    return HttpResponse.json({ message: 'Выход выполнен' }, { status: 200 })
  }),

  // ❌ Ошибка сервера (для теста 3.4)
  http.get('/api/v1/auth/me', ({ request }) => {
    if (request.headers.get('Authorization') === 'Bearer expired_token') {
      return HttpResponse.json({ detail: 'Токен истёк' }, { status: 401 })
    }
  }),
]

export const server = setupServer(...handlers)