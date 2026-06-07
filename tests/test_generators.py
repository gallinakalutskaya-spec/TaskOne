"""Тесты для модуля generators."""

import pytest
from src.generators import (
    filter_by_currency,
    transaction_descriptions,
    card_number_generator
)



# ФИКСТУРЫ


@pytest.fixture
def sample_transactions():
    """Фикстура с тестовыми данными транзакций."""
    return [
        {
            "id": 1,
            "operationAmount": {"currency": {"name": "USD"}},
            "description": "Перевод организации"
        },
        {
            "id": 2,
            "operationAmount": {"currency": {"name": "RUB"}},
            "description": "Оплата услуг"
        },
        {
            "id": 3,
            "operationAmount": {"currency": {"name": "USD"}},
            # Намеренно отсутствует ключ "description" для проверки устойчивости
        },
        {
            "id": 4,
            "operationAmount": {"currency": {"name": "EUR"}},
            "description": "Перевод с карты на карту"
        }
    ]



# ТЕСТЫ filter_by_currency


def test_filter_by_currency_correct_filtering(sample_transactions):
    """Проверяет, что функция корректно фильтрует транзакции по заданной валюте."""
    result = list(filter_by_currency(sample_transactions, "USD"))
    assert len(result) == 2
    assert result[0]["id"] == 1
    assert result[1]["id"] == 3


def test_filter_by_currency_absent_currency(sample_transactions):
    """Проверяет обработку случая, когда транзакции в заданной валюте отсутствуют."""
    result = list(filter_by_currency(sample_transactions, "GBP"))
    assert result == []


def test_filter_by_currency_empty_list():
    """Убеждается, что генератор не завершается ошибкой при обработке пустого списка."""
    result = list(filter_by_currency([], "USD"))
    assert result == []



# ТЕСТЫ transaction_descriptions


@pytest.mark.parametrize("tx_list, expected", [
    # Различное количество транзакций
    ([{"description": "One"}], ["One"]),
    ([{"description": "A"}, {"description": "B"}], ["A", "B"]),
    # Пустой список
    ([], []),
    # Отсутствие ключа description (проверка заглушки)
    ([{}], ["Описание отсутствует"]),
])
def test_transaction_descriptions_varying_inputs(tx_list, expected):
    """Тестирует работу функции с различным количеством входных данных и пустым списком."""
    result = list(transaction_descriptions(tx_list))
    assert result == expected



# ТЕСТЫ card_number_generator


@pytest.mark.parametrize("start, end, expected", [
    # Базовый диапазон с ведущими нулями
    (1, 3, ["0000 0000 0000 0001", "0000 0000 0000 0002", "0000 0000 0000 0003"]),
    # Проверка корректности форматирования в середине диапазона
    (1234567890123456, 1234567890123456, ["1234 5678 9012 3456"]),
    # Крайнее верхнее значение
    (9999999999999999, 9999999999999999, ["9999 9999 9999 9999"]),
    # Некорректный диапазон (start > end) должен корректно завершиться
    (10, 5, []),
])
def test_card_number_generator_ranges_and_formatting(start, end, expected):
    """Проверяет выдачу правильных номеров, форматирование и обработку крайних значений."""
    result = list(card_number_generator(start, end))
    assert result == expected