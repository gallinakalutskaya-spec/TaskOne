import pytest
from src.processing import filter_by_state, sort_by_date


@pytest.fixture
def sample_operations():
    """Фикстура с тестовыми данными для переиспользования в тестах."""
    return [
        {"id": 1, "state": "EXECUTED", "date": "2023-10-05T12:00:00"},
        {"id": 2, "state": "PENDING",  "date": "2023-11-01T09:30:00"},
        {"id": 3, "state": "EXECUTED", "date": "2023-09-20T15:45:00"},
        {"id": 4, "state": "CANCELLED","date": "2023-10-05T12:00:00"},
    ]


# ==================== filter_by_state ====================

@pytest.mark.parametrize(
    "search_state, expected_ids",
    [
        ("EXECUTED",    [1, 3]),
        ("PENDING",     [2]),
        ("CANCELLED",   [4]),
        ("NON_EXISTENT", []),  # Тест: статус отсутствует в списке
    ],
)
def test_filter_by_state(sample_operations, search_state, expected_ids):
    """Параметризованный тест фильтрации по разным статусам, включая отсутствующие."""
    result = filter_by_state(sample_operations, search_state)
    actual_ids = [op["id"] for op in result]
    assert actual_ids == expected_ids


def test_filter_by_state_empty_list():
    """Проверка работы функции с пустым списком."""
    assert filter_by_state([], "EXECUTED") == []


# ==================== sort_by_date ====================

def test_sort_by_date_descending(sample_operations):
    """Сортировка по убыванию (значение reverse=True по умолчанию)."""
    sorted_ops = sort_by_date(sample_operations)
    dates = [op["date"] for op in sorted_ops]
    assert dates == sorted(dates, reverse=True)


def test_sort_by_date_ascending(sample_operations):
    """Сортировка по возрастанию (reverse=False)."""
    sorted_ops = sort_by_date(sample_operations, reverse=False)