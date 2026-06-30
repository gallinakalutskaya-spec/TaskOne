"""Тестовый скрипт для проверки работы логгеров."""

from src.masks import get_mask_card_number, get_mask_account
from src.utils import read_json_file


def main():
    print("=== Тестирование логгеров ===\n")

    # Тест 1: Успешная маскировка карты
    print("Тест 1: Маскировка карты")
    try:
        result = get_mask_card_number("1234567890123456")
        print(f"Результат: {result}\n")
    except ValueError as e:
        print(f"Ошибка: {e}\n")

    # Тест 2: Ошибка маскировки карты (некорректный номер)
    print("Тест 2: Некорректный номер карты")
    try:
        result = get_mask_card_number("123")
        print(f"Результат: {result}\n")
    except ValueError as e:
        print(f"Ошибка: {e}\n")

    # Тест 3: Успешная маскировка счёта
    print("Тест 3: Маскировка счёта")
    try:
        result = get_mask_account("12345678901234567890")
        print(f"Результат: {result}\n")
    except ValueError as e:
        print(f"Ошибка: {e}\n")

    # Тест 4: Чтение существующего JSON-файла
    print("Тест 4: Чтение JSON-файла")
    transactions = read_json_file("data/operations.json")
    print(f"Прочитано записей: {len(transactions)}\n")

    # Тест 5: Чтение несуществующего файла
    print("Тест 5: Чтение несуществующего файла")
    transactions = read_json_file("nonexistent.json")
    print(f"Прочитано записей: {len(transactions)}\n")


if __name__ == "__main__":
    main()