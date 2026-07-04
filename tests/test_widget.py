# tests/test_widget.py
import pytest
from src.widget import mask_account_card, get_date


# ==================== mask_account_card ====================

@pytest.mark.parametrize("input_str, expected", [
    ("Visa Platinum 7000792289606361", "Visa Platinum 7000 79** **** 6361"),
    ("Maestro 1234567890123456", "Maestro 1234 56** **** 3456"),
    ("Счет 73654108430135874305", "Счет **4305"),
    ("МИР 2200123456789012", "МИР 2200 12** **** 9012"),
    ("Счет 00000000000000000001", "Счет **0001"),
])
def test_mask_account_card_valid(input_str, expected):
    """Параметризованный тест: корректное распознавание и маскировка разных типов карт/счетов."""
    assert mask_account_card(input_str) == expected


@pytest.mark.parametrize("invalid_input", [
    "Card 12345",           # Номер слишком короткий
    "Visa 123456789012345",  # 15 цифр
    "Visa 12345678901234567",  # 17 цифр
    "Счет 1234567890123456789",  # 19 цифр
    "Счет 123456789012345678901",  # 21 цифра
    "JustTextWithoutNum",   # Отсутствует номер
    "",                    # Пустая строка
])
def test_mask_account_card_invalid(invalid_input):
    """Тестирование на некорректные входные данные: функция должна выбрасывать ошибку."""
    with pytest.raises((ValueError, IndexError)):
        mask_account_card(invalid_input)


# ==================== get_date ====================

@pytest.mark.parametrize("input_date, expected", [
    ("2024-03-11T02:26:18.671407", "11.03.2024"),
    ("2023-12-31T23:59:59.999999", "31.12.2023"),
    ("2024-01-01T00:00:00.000000", "01.01.2024"),
    ("2000-02-29T12:00:00", "29.02.2000"),  # Високосный год
    ("1999-05-15T10:30:00", "15.05.1999"),  # Стандартная дата
])
def test_get_date_valid(input_date, expected):
    """Параметризованный тест: правильное преобразование валидных дат."""
    assert get_date(input_date) == expected


@pytest.mark.parametrize("invalid_date", [
    "",                  # Отсутствует дата
    "2024-03",           # Неполная дата
    "11.03.2024",        # Неверный формат (не ISO)
    "not_a_date",        # Строка без даты
    "2024/03/11 12:00",  # Другой разделитель
])
def test_get_date_invalid(invalid_date):
    """Тест на обработку отсутствующих или нестандартных дат."""
    with pytest.raises((IndexError, ValueError)):
        get_date(invalid_date)
