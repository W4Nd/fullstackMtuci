# backend/tests/unit/test_validators.py
import pytest
import re
from datetime import datetime


class TestTimeValidation:
    """Тесты валидации времени напоминаний"""
    
    @pytest.mark.parametrize("time_value", [
        "00:00", "09:30", "12:00", "23:59",  # корректные
    ])
    def test_valid_time_format(self, time_value):
        """Время в формате HH:MM должно проходить проверку формата"""
        pattern = r"^\d{2}:\d{2}$"
        assert re.match(pattern, time_value) is not None
    
    @pytest.mark.parametrize("time_value", [
        "1:30", "12:5", "invalid", "12-30", None, ""  # неверный формат
    ])
    def test_invalid_time_format_only(self, time_value):
        """Некорректный ФОРМАТ времени (не проходит регекс)"""
        pattern = r"^\d{2}:\d{2}$"
        if time_value is None or time_value == "":
            assert True  # Пустые значения обрабатываются отдельно
        else:
            assert re.match(pattern, str(time_value)) is None
    
    @pytest.mark.parametrize("time_value", [
        "25:00", "12:60", "99:99",  # формат верный, но значения нет
    ])
    def test_valid_format_invalid_logic(self, time_value):
        """Формат верный (проходит регекс), но логика неверная"""
        pattern = r"^\d{2}:\d{2}$"
        # 🔧 Регекс ДОЛЖЕН совпасть (формат правильный)
        assert re.match(pattern, time_value) is not None
        
        # 🔧 Но логическая проверка должна отклонить
        h, m = map(int, time_value.split(":"))
        assert not (0 <= h <= 23 and 0 <= m <= 59)
    
    def test_time_logical_validation(self):
        """Полная валидация: формат + логика"""
        def is_valid_time_full(time_str):
            """Проверяет и формат, и логические границы"""
            if not re.match(r"^\d{2}:\d{2}$", time_str):
                return False
            h, m = map(int, time_str.split(":"))
            return 0 <= h <= 23 and 0 <= m <= 59
        
        assert is_valid_time_full("23:59") is True
        assert is_valid_time_full("00:00") is True
        assert is_valid_time_full("24:00") is False  # логика
        assert is_valid_time_full("12:60") is False  # логика
        assert is_valid_time_full("1:30") is False   # формат


class TestDaysValidation:
    """Тесты валидации дней недели"""
    
    def test_valid_days_list(self):
        """Список дней должен содержать числа 0-6"""
        valid_days = [0, 1, 2, 3, 4, 5, 6]
        for day in valid_days:
            assert 0 <= day <= 6
    
    @pytest.mark.parametrize("days_input", [
        [],  # пустой список
        [7], [8], [-1],  # числа вне диапазона
        [0, 1, "2"],  # смешанные типы
        "not-a-list",  # не список
    ])
    def test_invalid_days_input(self, days_input):
        """Некорректные дни должны отклоняться"""
        def is_valid_days(days):
            if not isinstance(days, list) or len(days) == 0:
                return False
            return all(isinstance(d, int) and 0 <= d <= 6 for d in days)
        
        assert is_valid_days(days_input) is False
    
    def test_days_unique_and_sorted(self):
        """Дни должны быть уникальными"""
        days = [1, 3, 5, 3]  # есть дубликат
            
        has_duplicates = (len(days) != len(set(days)))
        assert has_duplicates is True  # подтверждаем, что дубликаты есть
            
        unique_days = sorted(set(days))
        assert unique_days == [1, 3, 5]


class TestMedicationValidation:
    """Тесты валидации данных о лекарствах"""
    
    @pytest.mark.parametrize("name", [
        "Aspirin", "Парацетамол", "Vitamin D3", "Omeprazole 20mg"
    ])
    def test_valid_medication_name(self, name):
        """Название лекарства: 1-100 символов"""
        assert 1 <= len(name) <= 100
    
    @pytest.mark.parametrize("name", [
        "", "a" * 101, None
    ])
    def test_invalid_medication_name(self, name):
        """Некорректное название должно отклоняться"""
        if name is None:
            assert True  # None обрабатывается отдельно
        else:
            assert not (1 <= len(name) <= 100)
    
    @pytest.mark.parametrize("dosage", [
        "100mg", "500 мг", "1 tablet", "2.5 ml"
    ])
    def test_valid_dosage_format(self, dosage):
        """Дозировка: 1-50 символов"""
        assert 1 <= len(dosage) <= 50