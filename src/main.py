"""Главный модуль проекта. Реализует интерактивное меню для работы с банковскими транзакциями."""

import csv
import json
import os
from typing import Any

from src.masks import get_mask_account, get_mask_card_number
from src.processing import filter_by_state, sort_by_date
from src.search import process_bank_search
from src.widget import get_date


# Константы
VALID_STATUSES = {"executed", "canceled", "pending"}
DISPLAY_STATUSES = {"executed": "EXECUTED", "canceled": "CANCELED", "pending": "PENDING"}


def load_transactions_from_json(file_path: str) -> list[dict[str, Any]]:
    """Загружает транзакции из JSON-файла."""
    if not os.path.exists(file_path):
        print(f"❌ Файл не найден: {file_path}")
        return []

    try:
        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)
            if not isinstance(data, list):
                print("❌ Файл содержит не список")
                return []
            return data
    except (json.JSONDecodeError, IOError) as e:
        print(f"❌ Ошибка чтения файла: {e}")
        return []


def load_transactions_from_csv(file_path: str) -> list[dict[str, Any]]:
    """Загружает транзакции из CSV-файла."""
    if not os.path.exists(file_path):
        print(f"❌ Файл не найден: {file_path}")
        return []

    try:
        transactions = []
        with open(file_path, "r", encoding="utf-8", newline="") as f:
            reader = csv.DictReader(f)
            for row in reader:
                transactions.append(dict(row))
        return transactions
    except IOError as e:
        print(f"❌ Ошибка чтения файла: {e}")
        return []


def load_transactions_from_xlsx(file_path: str) -> list[dict[str, Any]]:
    """Загружает транзакции из XLSX-файла."""
    try:
        import openpyxl
    except ImportError:
        print("❌ Для работы с XLSX установите библиотеку: poetry add openpyxl")
        return []

    if not os.path.exists(file_path):
        print(f"❌ Файл не найден: {file_path}")
        return []

    try:
        wb = openpyxl.load_workbook(file_path, read_only=True)
        ws = wb.active

        transactions = []
        headers = []
        for i, row in enumerate(ws.iter_rows(values_only=True)):
            if i == 0:
                headers = [str(cell) if cell else f"col_{j}" for j, cell in enumerate(row)]
                continue
            transactions.append(dict(zip(headers, row)))

        wb.close()
        return transactions
    except Exception as e:
        print(f"❌ Ошибка чтения файла: {e}")
        return []


def get_yes_no_input(prompt: str) -> bool:
    """Запрашивает у пользователя ответ Да/Нет. Возвращает True для 'да', False для 'нет'."""
    while True:
        answer = input(prompt).strip().lower()
        if answer in ("да", "yes", "y", "д"):
            return True
        if answer in ("нет", "no", "n", "н"):
            return False
        print("Пожалуйста, введите 'Да' или 'Нет'.")


def get_status_input() -> str:
    """Запрашивает у пользователя статус операции с валидацией."""
    while True:
        print('\nВведите статус, по которому необходимо выполнить фильтрацию.')
        print('Доступные для фильтровки статусы: EXECUTED, CANCELED, PENDING')
        status = input().strip().lower()

        if status in VALID_STATUSES:
            return status
        else:
            print(f'Статус операции "{status}" недоступен.')


def mask_field(field_value: str) -> str:
    """Маскирует номер карты или счёта в зависимости от длины."""
    if not field_value:
        return ""

    # Извлекаем цифры из строки
    digits = "".join(filter(str.isdigit, field_value))

    if len(digits) == 16:
        return get_mask_card_number(digits)
    elif len(digits) == 20:
        return get_mask_account(digits)
    else:
        return field_value


def format_transaction(transaction: dict[str, Any]) -> str:
    """Форматирует транзакцию для вывода в консоль."""
    # Дата
    date_str = transaction.get("date", "")
    try:
        formatted_date = get_date(date_str)
    except (ValueError, IndexError):
        formatted_date = "Дата неизвестна"

    # Описание
    description = transaction.get("description", "Операция")

    # From и To
    from_field = transaction.get("from", "")
    to_field = transaction.get("to", "")

    masked_from = mask_field(from_field) if from_field else ""
    masked_to = mask_field(to_field) if to_field else ""

    # Сумма и валюта
    operation_amount = transaction.get("operationAmount", {})
    amount = operation_amount.get("amount", "0")
    currency_name = operation_amount.get("currency", {}).get("name", "")

    # Формируем строку
    lines = [f"{formatted_date} {description}"]

    if masked_from and masked_to:
        lines.append(f"{masked_from} -> {masked_to}")
    elif masked_to:
        lines.append(masked_to)
    elif masked_from:
        lines.append(masked_from)

    lines.append(f"Сумма: {amount} {currency_name}")

    return "\n".join(lines)


def main() -> None:
    """Главная функция программы. Реализует интерактивное меню."""
    print("Привет! Добро пожаловать в программу работы с банковскими транзакциями.")
    print("Выберите необходимый пункт меню:")
    print("1. Получить информацию о транзакциях из JSON-файла")
    print("2. Получить информацию о транзакциях из CSV-файла")
    print("3. Получить информацию о транзакциях из XLSX-файла")

    while True:
        choice = input().strip()
        if choice in ("1", "2", "3"):
            break
        print("Пожалуйста, введите 1, 2 или 3.")

    # Загрузка данных
    if choice == "1":
        print("\nДля обработки выбран JSON-файл.")
        file_path = "data/operations.json"
        transactions = load_transactions_from_json(file_path)
    elif choice == "2":
        print("\nДля обработки выбран CSV-файл.")
        file_path = input("Введите путь к CSV-файлу: ").strip() or "data/operations.csv"
        transactions = load_transactions_from_csv(file_path)
    elif choice == "3":
        print("\nДля обработки выбран XLSX-файл.")
        file_path = input("Введите путь к XLSX-файлу: ").strip() or "data/operations.xlsx"
        transactions = load_transactions_from_xlsx(file_path)

    if not transactions:
        print("\n❌ Не удалось загрузить транзакции. Завершение программы.")
        return

    print(f"\n✅ Успешно загружено транзакций: {len(transactions)}")

    # Фильтрация по статусу
    status = get_status_input()
    transactions = filter_by_state(transactions, status.upper())
    print(f'\nОперации отфильтрованы по статусу "{DISPLAY_STATUSES[status]}"')

    if not transactions:
        print("\nНе найдено ни одной транзакции, подходящей под ваши условия фильтрации")
        return

    # Сортировка по дате
    if get_yes_no_input("\nОтсортировать операции по дате? Да/Нет\n"):
        while True:
            order = input("Отсортировать по возрастанию или по убыванию?\n").strip().lower()
            if "возраст" in order:
                transactions = sort_by_date(transactions, reverse=False)
                break
            elif "убыв" in order:
                transactions = sort_by_date(transactions, reverse=True)
                break
            else:
                print('Пожалуйста, введите "по возрастанию" или "по убыванию".')

    # Фильтр по рублевым транзакциям
    if get_yes_no_input("\nВыводить только рублевые транзакции? Да/Нет\n"):
        transactions = [
            t for t in transactions
            if t.get("operationAmount", {}).get("currency", {}).get("code") == "RUB"
        ]

    if not transactions:
        print("\nНе найдено ни одной транзакции, подходящей под ваши условия фильтрации")
        return

    # Поиск по слову в описании
    if get_yes_no_input("\nОтфильтровать список транзакций по определенному слову в описании? Да/Нет\n"):
        search_word = input("Введите слово для поиска: ").strip()
        if search_word:
            transactions = process_bank_search(transactions, search_word)

    if not transactions:
        print("\nНе найдено ни одной транзакции, подходящей под ваши условия фильтрации")
        return

    # Вывод результата
    print("\nРаспечатываю итоговый список транзакций...")
    print(f"\nВсего банковских операций в выборке: {len(transactions)}\n")

    for transaction in transactions:
        print(format_transaction(transaction))
        print()


if __name__ == "__main__":
    main()
    