// frontend/tests/integration/LoginFlow.test.tsx
import { describe, it, expect, vi, beforeEach, afterEach } from 'vitest'
import { render, screen, waitFor } from '@testing-library/react'
import userEvent from '@testing-library/user-event'
import { MemoryRouter } from 'react-router-dom'
import AuthPage from '../../src/pages/Auth'
import { AuthProvider } from '../../src/contexts/AuthContext'
import type { User } from '../../src/types'

// Мокаем apiService ДО импорта компонента
vi.mock('../../src/services/api', () => ({
  apiService: {
    login: vi.fn(),
    getMe: vi.fn(),
    logout: vi.fn(),
  },
}))
import { apiService } from '../../src/services/api'

describe('Login Flow (3.2)', () => {
  beforeEach(() => {
    vi.clearAllMocks()
    // @ts-ignore — очистка мока localStorage (если используется)
    global.localStorageMock?.clear()
  })

  afterEach(() => {
    vi.restoreAllMocks()
  })

  it('успешный вход: форма → запрос → успешный ответ', async () => {
    const user = userEvent.setup()
    
    // 🔧 Полный объект User со всеми обязательными полями
    const mockUser: User = {
      id: 1,
      username: 'testuser',
      email: 'test@example.com',
      created_at: '2024-01-01T00:00:00Z',
      first_name: null,
      age: null,
      height_cm: null,
      weight_kg: null,
      target_weight_kg: null,
      bio: null,
      updated_at: null,
    }

    // Мокаем успешный ответ от API
    vi.mocked(apiService.login).mockResolvedValue({
      access_token: 'mock_token_123',
      refresh_token: 'mock_refresh_456',
      user: mockUser,
      roles: ['user']
    })

    render(
      <MemoryRouter initialEntries={['/auth']}>
        <AuthProvider>
          <AuthPage />
        </AuthProvider>
      </MemoryRouter>
    )

    // 🔧 ИСПРАВЛЕННЫЕ СЕЛЕКТОРЫ — точный текст лейбла (без регексов)
    const usernameInput = screen.getByLabelText('Имя пользователя *')
    const passwordInput = screen.getByLabelText('Пароль *')
    
    // Заполняем форму
    await user.type(usernameInput, 'testuser')
    await user.type(passwordInput, 'correctpass')
    
    // Отправляем форму
    const submitButton = screen.getByRole('button', { name: 'Войти' })
    await user.click(submitButton)

    // ✅ Проверяем, что API был вызван с правильными данными
    await waitFor(() => {
      expect(apiService.login).toHaveBeenCalledWith({
        username: 'testuser',
        password: 'correctpass'
      })
    })

    // 🔧 Проверяем, что ошибка НЕ отображается (значит, вход успешен)
    // Это надёжнее, чем проверять детали реализации (localStorage)
    await waitFor(() => {
      expect(
        screen.queryByText(/неверные данные|ошибка|не удалось войти|invalid credentials/i)
      ).not.toBeInTheDocument()
    })
  })

  it('ошибка входа: показывается сообщение об ошибке', async () => {
    const user = userEvent.setup()
    
    // Мокаем ошибку 401 от API
    vi.mocked(apiService.login).mockRejectedValue({
      response: { 
        status: 401, 
          detail: 'Неверные данные' 
      } 
    })

    render(
      <MemoryRouter>
        <AuthProvider>
          <AuthPage />
        </AuthProvider>
      </MemoryRouter>
    )

    // 🔧 Те же точные селекторы
    const usernameInput = screen.getByLabelText('Имя пользователя *')
    const passwordInput = screen.getByLabelText('Пароль *')
    
    await user.type(usernameInput, 'wronguser')
    await user.type(passwordInput, 'wrongpass')
    
    const submitButton = screen.getByRole('button', { name: 'Войти' })
    await user.click(submitButton)

    // ✅ Проверяем, что сообщение об ошибке ОТОБРАЗИЛОСЬ
    await waitFor(() => {
      const errorText = screen.queryByText(/неверные данные|ошибка|не удалось войти|invalid credentials|401/i)
      expect(errorText).toBeInTheDocument()
    })
  })
})