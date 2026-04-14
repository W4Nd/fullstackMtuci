import React, { useState, useEffect, useCallback } from 'react';
import { useSearchParams } from 'react-router-dom';
import axios from 'axios';
import SEO from '../components/SEO';
import ReminderForm from '../components/ReminderForm';
import ReminderList from '../components/ReminderList';
import type { Reminder, NewReminder, PaginatedRemindersResponse } from '../types';

const API_BASE_URL = 'http://127.0.0.1:8000/api/v1';

interface Filters {
  search: string;
  day: number | null;
  is_active: boolean | null;
  sort_by: 'time' | 'created_at';
  sort_dir: 'asc' | 'desc';
  page: number;
  page_size: number;
}

const HomePage: React.FC = () => {
  const [searchParams, setSearchParams] = useSearchParams();

  const [reminders, setReminders] = useState<Reminder[]>([]);
  const [total, setTotal] = useState(0);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const getFiltersFromUrl = (): Filters => {
    return {
      search: searchParams.get('search') || '',
      day: searchParams.get('day') ? Number(searchParams.get('day')) : null,
      is_active:
        searchParams.get('is_active') === 'true'
          ? true
          : searchParams.get('is_active') === 'false'
          ? false
          : null,
      sort_by: (searchParams.get('sort_by') as 'time' | 'created_at') || 'time',
      sort_dir: (searchParams.get('sort_dir') as 'asc' | 'desc') || 'asc',
      page: Number(searchParams.get('page')) || 1,
      page_size: Number(searchParams.get('page_size')) || 10,
    };
  };

  const [filters, setFilters] = useState<Filters>(getFiltersFromUrl);

  useEffect(() => {
    setFilters(getFiltersFromUrl());
  }, [searchParams.toString()]);

  const fetchReminders = useCallback(async () => {
    setLoading(true);
    setError(null);

    try {
      const params = new URLSearchParams({
        ...(filters.search && { search: filters.search }),
        ...(filters.day !== null && { day: filters.day.toString() }),
        ...(filters.is_active !== null && { is_active: filters.is_active.toString() }),
        sort_by: filters.sort_by,
        sort_dir: filters.sort_dir,
        page: filters.page.toString(),
        page_size: filters.page_size.toString(),
      });

      const token = localStorage.getItem('auth_access_token');

      const response = await axios.get<PaginatedRemindersResponse>(
        `${API_BASE_URL}/reminders?${params.toString()}`,
        {
          headers: token ? { Authorization: `Bearer ${token}` } : undefined,
        }
      );

      setReminders(response.data.items); 
      setTotal(response.data.total);
    } catch (err) {
      console.error(err);
      setError('Ошибка загрузки напоминаний');
    } finally {
      setLoading(false);
    }
  }, [filters]);

  useEffect(() => {
    fetchReminders();
  }, [fetchReminders]);

  const updateFilters = (newFilters: Partial<Filters>) => {
    const updated: Filters = { ...filters, ...newFilters };

    // При смене фильтров всегда возвращаемся на первую страницу
    if (
      newFilters.search !== undefined ||
      newFilters.day !== undefined ||
      newFilters.is_active !== undefined ||
      newFilters.sort_by !== undefined ||
      newFilters.sort_dir !== undefined ||
      newFilters.page_size !== undefined
    ) {
      updated.page = 1;
    }

    setFilters(updated);

    const params = new URLSearchParams();
    if (updated.search) params.set('search', updated.search);
    if (updated.day !== null) params.set('day', updated.day.toString());
    if (updated.is_active !== null) params.set('is_active', updated.is_active.toString());
    params.set('sort_by', updated.sort_by);
    params.set('sort_dir', updated.sort_dir);
    params.set('page', updated.page.toString());
    params.set('page_size', updated.page_size.toString());

    setSearchParams(params, { replace: true });
  };

  const handleSearch = (search: string) => updateFilters({ search });
  const handleDayFilter = (day: number | null) => updateFilters({ day });
  const handleActiveFilter = (is_active: boolean | null) => updateFilters({ is_active });

  const handleSort = (sort_by: 'time' | 'created_at') => {
    const sort_dir: 'asc' | 'desc' =
      filters.sort_by === sort_by && filters.sort_dir === 'asc' ? 'desc' : 'asc';
    updateFilters({ sort_by, sort_dir });
  };

  const handlePageChange = (page: number) => updateFilters({ page });
  const handlePageSizeChange = (page_size: number) => updateFilters({ page_size });

  const handleAddReminder = async (data: NewReminder) => {
    try {
      const token = localStorage.getItem('auth_access_token');
      await axios.post(`${API_BASE_URL}/reminders`, data, {
        headers: token ? { Authorization: `Bearer ${token}` } : undefined,
      });
      fetchReminders();
    } catch (err) {
      console.error(err);
      alert('Ошибка создания напоминания');
    }
  };

  const handleToggle = async (id: number) => {
    try {
      const token = localStorage.getItem('auth_access_token');
      await axios.post(
        `${API_BASE_URL}/reminders/${id}/toggle`,
        {},
        {
          headers: token ? { Authorization: `Bearer ${token}` } : undefined,
        }
      );
      fetchReminders();
    } catch (err) {
      console.error(err);
      alert('Ошибка переключения статуса');
    }
  };

  const handleDelete = async (id: number) => {
    if (!confirm('Удалить напоминание?')) return;
    try {
      const token = localStorage.getItem('auth_access_token');
      await axios.delete(`${API_BASE_URL}/reminders/${id}`, {
        headers: token ? { Authorization: `Bearer ${token}` } : undefined,
      });
      fetchReminders();
    } catch (err) {
      console.error(err);
      alert('Ошибка удаления');
    }
  };

    const dayNames = ['Пн', 'Вт', 'Ср', 'Чт', 'Пт', 'Сб', 'Вс'];
    
    const jsonLd = {
        "@context": "https://schema.org",
        "@type": "WebApplication",
        "name": "Medication Reminder",
        "description": "Приложение для управления расписанием приёма лекарств и напоминаний",
        "applicationCategory": "HealthApplication",
        "operatingSystem": "Web",
        "browserRequirements": "Requires JavaScript",
        "url": "https://yourdomain.com/",
        "offers": {
          "@type": "Offer",
          "price": "0",
          "priceCurrency": "RUB"
        },
        "featureList": [
          "Напоминания по расписанию",
          "Фильтрация по дням недели",
          "Управление статусами",
          "Поиск по названию лекарства"
        ]
      };
    
      return (
        <>
          <SEO
            title="Мои напоминания"
            description="Управляйте расписанием приёма лекарств: создавайте, фильтруйте и отслеживайте напоминания"
            canonical="/"
            jsonLd={jsonLd}
          />
          
          {/* 4. Семантический main с aria-label */}
          <main 
            style={{ maxWidth: '1200px', margin: '0 auto', padding: '1rem' }}
            role="main"
            aria-label="Управление напоминаниями о лекарствах"
          >
            {/* 5. Заголовок страницы — только один h1 */}
            <header style={{ marginBottom: '2rem' }}>
              <h1 style={{ fontSize: '2rem', fontWeight: 'bold' }}>
                Мои напоминания о лекарствах
              </h1>
              <p style={{ color: '#6b7280', marginTop: '0.5rem' }}>
                Создавайте и отслеживайте расписание приёма препаратов
              </p>
            </header>
    
            {/* 6. Секция фильтров с семантической разметкой */}
            <section 
              aria-labelledby="filters-heading"
              style={{
                background: 'white',
                borderRadius: '8px',
                padding: '1.5rem',
                marginBottom: '1.5rem',
                boxShadow: '0 2px 10px rgba(0,0,0,0.1)',
              }}
            >
              <h2 id="filters-heading" style={{ fontSize: '1.25rem', marginBottom: '1rem' }}>
                Фильтры
              </h2>
              
              <div style={{
                display: 'grid',
                gridTemplateColumns: 'repeat(auto-fit, minmax(200px, 1fr))',
                gap: '1rem',
              }}>
                {/* Поиск по названию */}
                <div>
                  <label htmlFor="search-input">Поиск по лекарству</label>
                  <input
                    id="search-input"
                    type="text"
                    value={filters.search}
                    onChange={(e) => handleSearch(e.target.value)}
                    placeholder="Введите название..."
                    style={{
                      width: '100%',
                      padding: '0.5rem',
                      border: '1px solid #d1d5db',
                      borderRadius: '4px',
                    }}
                    aria-describedby="search-hint"
                  />
                  <span id="search-hint" className="sr-only">
                    Введите часть названия лекарства для поиска
                  </span>
                </div>
    
                {/* День недели */}
                <div>
                  <label htmlFor="day-select">День недели</label>
                  <select
                    id="day-select"
                    value={filters.day === null ? '' : filters.day}
                    onChange={(e) =>
                      handleDayFilter(e.target.value === '' ? null : Number(e.target.value))
                    }
                    style={{
                      width: '100%',
                      padding: '0.5rem',
                      border: '1px solid #d1d5db',
                      borderRadius: '4px',
                    }}
                  >
                    <option value="">Все дни</option>
                    {dayNames.map((day, i) => (
                      <option key={i} value={i}>{day}</option>
                    ))}
                  </select>
                </div>
    
                {/* Статус */}
                <div>
                  <label htmlFor="status-select">Статус</label>
                  <select
                    id="status-select"
                    value={filters.is_active === null ? '' : filters.is_active.toString()}
                    onChange={(e) => {
                      const val = e.target.value;
                      handleActiveFilter(val === '' ? null : val === 'true');
                    }}
                    style={{
                      width: '100%',
                      padding: '0.5rem',
                      border: '1px solid #d1d5db',
                      borderRadius: '4px',
                    }}
                  >
                    <option value="">Все</option>
                    <option value="true">Активные</option>
                    <option value="false">Выключенные</option>
                  </select>
                </div>
    
                {/* Сортировка */}
                <div>
                  <label>Сортировка</label>
                  <div style={{ display: 'flex', gap: '0.5rem' }} role="group" aria-label="Сортировка напоминаний">
                    <button
                      onClick={() => handleSort('time')}
                      aria-pressed={filters.sort_by === 'time'}
                      style={{
                        flex: 1,
                        padding: '0.5rem',
                        border: filters.sort_by === 'time' ? '2px solid #2563eb' : '1px solid #d1d5db',
                        background: filters.sort_by === 'time' ? '#dbeafe' : 'white',
                        borderRadius: '4px',
                        cursor: 'pointer',
                      }}
                    >
                      {filters.sort_by === 'time'
                        ? filters.sort_dir === 'asc' ? 'Время ↑' : 'Время ↓'
                        : 'Время'}
                    </button>
                    <button
                      onClick={() => handleSort('created_at')}
                      aria-pressed={filters.sort_by === 'created_at'}
                      style={{
                        flex: 1,
                        padding: '0.5rem',
                        border: filters.sort_by === 'created_at' ? '2px solid #2563eb' : '1px solid #d1d5db',
                        background: filters.sort_by === 'created_at' ? '#dbeafe' : 'white',
                        borderRadius: '4px',
                        cursor: 'pointer',
                      }}
                    >
                      {filters.sort_by === 'created_at'
                        ? filters.sort_dir === 'asc' ? 'Дата ↑' : 'Дата ↓'
                        : 'Дата'}
                    </button>
                  </div>
                </div>
    
                {/* Размер страницы */}
                <div>
                  <label htmlFor="pagesize-select">На странице</label>
                  <select
                    id="pagesize-select"
                    value={filters.page_size}
                    onChange={(e) => handlePageSizeChange(Number(e.target.value))}
                    style={{
                      width: '100%',
                      padding: '0.5rem',
                      border: '1px solid #d1d5db',
                      borderRadius: '4px',
                    }}
                  >
                    <option value={5}>5</option>
                    <option value={10}>10</option>
                    <option value={20}>20</option>
                    <option value={50}>50</option>
                  </select>
                </div>
              </div>
            </section>
    
            {/* 7. Секция создания напоминания */}
            <section aria-labelledby="add-reminder-heading" style={{ marginBottom: '1.5rem' }}>
              <h2 id="add-reminder-heading" className="sr-only">Добавить новое напоминание</h2>
              <ReminderForm onSubmit={handleAddReminder} />
            </section>
    
            {/* Состояния загрузки / ошибки */}
            {loading && (
              <div role="status" aria-live="polite" style={{ padding: '1rem', textAlign: 'center' }}>
                Загрузка напоминаний...
              </div>
            )}
            
            {error && (
              <div role="alert" style={{ color: 'red', padding: '1rem', background: '#fef2f2', borderRadius: '4px' }}>
                {error}
              </div>
            )}
    
            {/* 8. Секция списка напоминаний */}
            <section aria-labelledby="reminders-list-heading">
              <h2 id="reminders-list-heading" className="sr-only">Список напоминаний</h2>
              <ReminderList 
                reminders={reminders} 
                onToggle={handleToggle} 
                onDelete={handleDelete} 
              />
            </section>
    
            {/* Пагинатор */}
            {total > 0 && (
              <nav 
                aria-label="Пагинация списка напоминаний"
                style={{
                  display: 'flex',
                  justifyContent: 'center',
                  alignItems: 'center',
                  gap: '1rem',
                  marginTop: '2rem',
                  background: 'white',
                  padding: '1rem',
                  borderRadius: '8px',
                  boxShadow: '0 2px 10px rgba(0,0,0,0.1)',
                }}
              >
                <div>Всего: {total}</div>
                <div style={{ display: 'flex', gap: '0.5rem' }}>
                  <button
                    onClick={() => handlePageChange(filters.page - 1)}
                    disabled={filters.page <= 1}
                    aria-label="Предыдущая страница"
                    style={{
                      padding: '0.5rem 1rem',
                      border: '1px solid #d1d5db',
                      background: 'white',
                      borderRadius: '4px',
                      cursor: filters.page <= 1 ? 'not-allowed' : 'pointer',
                    }}
                  >
                    ← Назад
                  </button>
                  <span aria-live="polite">
                    Страница {filters.page} из {Math.ceil(total / filters.page_size)}
                  </span>
                  <button
                    onClick={() => handlePageChange(filters.page + 1)}
                    disabled={filters.page * filters.page_size >= total}
                    aria-label="Следующая страница"
                    style={{
                      padding: '0.5rem 1rem',
                      border: '1px solid #d1d5db',
                      background: 'white',
                      borderRadius: '4px',
                      cursor: filters.page * filters.page_size >= total ? 'not-allowed' : 'pointer',
                    }}
                  >
                    Вперёд →
                  </button>
                </div>
              </nav>
            )}
          </main>
        </>
      );
    };
    
    export default HomePage;
