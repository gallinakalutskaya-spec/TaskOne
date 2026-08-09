"""Модуль для поиска и категоризации банковских операций с использованием регулярных выражений."""

import re
from typing import Any


def process_bank_search(data: list[dict[str, Any]], search: str) -> list[dict[str, Any]]:
    """
    Фильтрует список транзакций по строке поиска в описании.

    Использует регулярные выражения для нечувствительного к регистру поиска.

    Args:
        data: Список словарей с данными о транзакциях.
        search: Строка для поиска в описании.

    Returns:
        Список словарей, у которых в поле 'description' найдена искомая строка.

    Example:
        >>> data = [{"description": "Перевод организации"}, {"description": "Открытие вклада"}]
        >>> process_bank_search(data, "перевод")
        [{'description': 'Перевод организации'}]
    """
    if not search:
        return data

    # Компилируем регулярное выражение (флаг re.IGNORECASE для нечувствительности к регистру)
    pattern = re.compile(re.escape(search), re.IGNORECASE)

    result = []
    for transaction in data:
        description = transaction.get("description", "")
        if pattern.search(description):
            result.append(transaction)

    return result


def process_bank_operations(data: list[dict[str, Any]], categories: list[str]) -> dict[str, int]:
    """
    Подсчитывает количество операций в каждой категории.

    Категория определяется по наличию названия категории в поле 'description'.

    Args:
        data: Список словарей с данными о транзакциях.
        categories: Список названий категорий для подсчёта.

    Returns:
        Словарь, где ключи — названия категорий, значения — количество операций.

    Example:
        >>> data = [
        ...     {"description": "Перевод организации"},
        ...     {"description": "Перевод со счета на счет"},
        ...     {"description": "Открытие вклада"}
        ... ]
        >>> process_bank_operations(data, ["Перевод", "Открытие"])
        {'Перевод': 2, 'Открытие': 1}
    """
    # Инициализируем счётчики нулями для всех категорий
    result = {category: 0 for category in categories}

    for transaction in data:
        description = transaction.get("description", "")
        for category in categories:
            # Используем re.search для поиска категории в описании
            pattern = re.compile(re.escape(category), re.IGNORECASE)
            if pattern.search(description):
                result[category] += 1
                break  # Одна транзакция = одна категория

    return result
