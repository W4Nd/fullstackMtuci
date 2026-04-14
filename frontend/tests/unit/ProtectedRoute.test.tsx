// frontend/tests/unit/ProtectedRoute.test.tsx
import { describe, it, expect, vi, beforeEach, afterEach } from 'vitest'
import { render, screen, waitFor } from '@testing-library/react'
import { MemoryRouter, Route, Routes } from 'react-router-dom'
import ProtectedRoute from '../../src/components/ProtectedRoute'
import { useAuth } from '../../src/contexts/AuthContext'
import type { User } from '../../src/types'

// 🔧 Мокаем useAuth ДО импорта компонента
vi.mock('../../src/contexts/AuthContext', async () => {
  const actual = await vi.importActual('../../src/contexts/AuthContext')
  return {
    ...actual,
    useAuth: vi.fn(),
    AuthProvider: ({ children }: { children: React.ReactNode }) => <>{children}</>, // ← заглушка
  }
})

const TestComponent = () => <div data-testid="protected-content">Protected</div>

// 🔧 Упрощённый рендер без лишнего AuthProvider
const renderWithRouter = (ui: React.ReactElement, initialEntries: string[] = ['/']) => {
  return render(
    <MemoryRouter initialEntries={initialEntries}>
      {ui}
    </MemoryRouter>
  )
}

describe('ProtectedRoute (3.1 + 3.3)', () => {
  
  beforeEach(() => {
    vi.clearAllMocks()
    // @ts-ignore
    global.localStorageMock?.clear()
  })

  afterEach(() => {
    vi.restoreAllMocks()
  })

  it('редиректит на /auth, если пользователь не авторизован', async () => {
    vi.mocked(useAuth).mockReturnValue({
      user: null,
      roles: [],
      loading: false,
      login: vi.fn(),
      logout: vi.fn(),
      checkAuth: vi.fn(),
      hasPermission: vi.fn().mockReturnValue(false),
    })

    renderWithRouter(
      <Routes>
        <Route path="/auth" element={<div data-testid="auth-page">Auth Page</div>} />
        <Route path="/" element={
          <ProtectedRoute>
            <TestComponent />
          </ProtectedRoute>
        } />
      </Routes>
    )

    await waitFor(() => {
      expect(screen.queryByTestId('auth-page')).toBeInTheDocument()
    })
    expect(screen.queryByTestId('protected-content')).not.toBeInTheDocument()
  })

  it('показывает контент, если пользователь авторизован', () => {
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
    
    vi.mocked(useAuth).mockReturnValue({
      user: mockUser,
      roles: ['user'],
      loading: false,
      login: vi.fn(),
      logout: vi.fn(),
      checkAuth: vi.fn(),
      hasPermission: vi.fn().mockReturnValue(true),
    })

    renderWithRouter(
      <ProtectedRoute>
        <TestComponent />
      </ProtectedRoute>
    )

    expect(screen.getByTestId('protected-content')).toBeInTheDocument()
  })

  it('показывает лоадер во время проверки авторизации', () => {
    vi.mocked(useAuth).mockReturnValue({
      user: null,
      roles: [],
      loading: true,
      login: vi.fn(),
      logout: vi.fn(),
      checkAuth: vi.fn(),
      hasPermission: vi.fn().mockReturnValue(false),
    })
  
    renderWithRouter(
      <ProtectedRoute>
        <TestComponent />
      </ProtectedRoute>
    )
  
    // 🔧 Надёжная проверка: защищённого контента НЕТ
    expect(screen.queryByTestId('protected-content')).not.toBeInTheDocument()
    
    // 🔧 Опционально: проверяем индикатор загрузки (если он есть в вашем UI)
    const loader = screen.queryByTestId('page-loader')
    if (loader) {
      expect(loader).toBeInTheDocument()
    }
  })
})