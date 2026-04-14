import { useState } from 'react';
import { ExternalAPI } from '../services/externalApi';

interface DrugResult {
  brand_name?: string[];
  purpose?: string[];
  warnings?: string[];
}

const DrugSearch = () => {
  const [query, setQuery] = useState('');
  const [results, setResults] = useState<DrugResult[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [fallback, setFallback] = useState(false);

  const handleSearch = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!query.trim()) return;
    
    setLoading(true);
    setError(null);
    setFallback(false);
    
    try {
      const { data } = await ExternalAPI.searchDrug(query.trim());
      
      if (data.fallback) {
        setFallback(true);
        return;
      }
      
      setResults(data.results || []);
      if (data.count === 0) {
        setError('Лекарство не найдено в базе FDA');
      }
    } catch (err) {
      setError('Не удалось загрузить данные. Попробуйте позже.');
      console.error('Drug search error:', err);
    } finally {
      setLoading(false);
    }
  };

  return (
    <section aria-labelledby="drug-search-heading">
      <h2 id="drug-search-heading">Поиск лекарства</h2>
      
      <form onSubmit={handleSearch} className="drug-search-form">
        <label htmlFor="drug-query" className="sr-only">Название лекарства</label>
        <input
          id="drug-query"
          type="text"
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          placeholder="Например: Aspirin"
          disabled={loading}
          aria-busy={loading}
        />
        <button type="submit" disabled={loading || !query.trim()}>
          {loading ? 'Поиск...' : 'Найти'}
        </button>
      </form>

      {/* Состояния */}
      {loading && (
        <div role="status" aria-live="polite" className="loading">
          Загрузка информации...
        </div>
      )}
      
      {fallback && (
        <div role="alert" className="alert-info">
          ⚠️ Данные о лекарствах временно недоступны. 
          Проверьте информацию у врача.
        </div>
      )}
      
      {error && !loading && (
        <div role="alert" className="alert-error">
          {error}
        </div>
      )}
      
      {/* Результаты */}
      <ul className="drug-results" aria-live="polite">
        {results.map((drug, idx) => (
          <li key={idx} className="drug-card">
            <h3>{drug.brand_name?.[0] || 'Без названия'}</h3>
            {drug.purpose && (
              <p><strong>Назначение:</strong> {drug.purpose[0]}</p>
            )}
            {drug.warnings && (
              <details>
                <summary>⚠️ Предупреждения</summary>
                <ul>
                  {drug.warnings.slice(0, 3).map((w, i) => (
                    <li key={i}>{w}</li>
                  ))}
                </ul>
              </details>
            )}
          </li>
        ))}
      </ul>
    </section>
  );
};

export default DrugSearch;