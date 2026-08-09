"""Тесты для модуля search."""

import pytest
from src.search import process_bank_search, process_bank_operations


@pytest.fixture
def sample_transactions():
    """Фикстура с тестовыми транзакциями."""
    return [
        {"id": 1, "description": "Перевод организации"},
        {"id": 2, "description": "Перевод со счета на счет"},
        {"id": 3, "description": "Открытие вклада"},
        {"id": 4, "description": "Перевод с карты на карту"},
        {"id": 5, "description": "Оплата услуг"},
    ]


class TestProcessBankSearch:
    """Тесты для функции process_bank_search."""

    def test_search_found(self, sample_transactions):
        """Поиск строки, которая есть в описаниях."""
        result = process_bank_search(sample_transactions, "Перевод")
        assert len(result) == 3
        assert all("Перевод" in t["description"] for t in result)

    def test_search_case_insensitive(self, sample_transactions):
        """Поиск должен быть нечувствителен к регистру."""
        result = process_bank_search(sample_transactions, "перевод")
        assert len(result) == 3

    def test_search_not_found(self, sample_transactions):
        """Поиск строки, которой нет."""
        result = process_bank_search(sample_transactions, "несуществующее")
        assert result == []

    def test_search_empty_query(self, sample_transactions):
        """Пустая строка поиска возвращает все транзакции."""
        result = process_bank_search(sample_transactions, "")
        assert result == sample_transactions

    def test_search_empty_data(self):
        """Пустой список транзакций."""
        result = process_bank_search([], "Перевод")
        assert result == []

    def test_search_missing_description(self):
        """Транзакция без поля description не должна вызывать ошибку."""
        data = [{"id": 1}, {"id": 2, "description": "Перевод"}]
        result = process_bank_search(data, "Перевод")
        assert len(result) == 1
        assert result[0]["id"] == 2


class TestProcessBankOperations:
    """Тесты для функции process_bank_operations."""

    def test_count_categories(self, sample_transactions):
        """Подсчёт операций по категориям."""
        result = process_bank_operations(
            sample_transactions,
            ["Перевод", "Открытие", "Оплата"]
        )
        assert result == {"Перевод": 3, "Открытие": 1, "Оплата": 1}

    def test_category_not_found(self, sample_transactions):
        """Категория, которой нет в описаниях."""
        result = process_bank_operations(
            sample_transactions,
            ["Несуществующая"]
        )
        assert result == {"Несуществующая": 0}

    def test_empty_data(self):
        """Пустой список транзакций."""
        result = process_bank_operations([], ["Перевод"])
        assert result == {"Перевод": 0}

    def test_empty_categories(self, sample_transactions):
        """Пустой список категорий."""
        result = process_bank_operations(sample_transactions, [])
        assert result == {}

    def test_case_insensitive(self, sample_transactions):
        """Поиск категорий нечувствителен к регистру."""
        result = process_bank_operations(
            sample_transactions,
            ["перевод"]
        )
        assert result == {"перевод": 3}
        