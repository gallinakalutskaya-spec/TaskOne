"""Модуль с генераторами для обработки банковских данных."""

from typing import Iterator


def filter_by_currency(transactions: list[dict], currency: str) -> Iterator[dict]:
    """
    Возвращает итератор транзакций, у которых валюта совпадает с заданной.
    """
    for transaction in transactions:
        # Безопасное извлечение вложенного значения
        txn_currency = transaction.get("operationAmount", {}).get("currency", {}).get("name")
        if txn_currency == currency:
            yield transaction


def transaction_descriptions(transactions: list[dict]) -> Iterator[str]:
    """
    Генератор, который поочередно возвращает описание каждой транзакции.
    """
    for transaction in transactions:
        # Если ключа нет, возвращаем заглушку, чтобы генератор не падал
        yield transaction.get("description", "Описание отсутствует")


def card_number_generator(start: int, end: int) -> Iterator[str]:
    """
    Генератор номеров банковских карт в заданном диапазоне.
    Формат: XXXX XXXX XXXX XXXX
    """
    # Защита от некорректных диапазонов
    start = max(1, start)
    end = min(9_999_999_999_999_999, end)

    for number in range(start, end + 1):
        # Форматируем число в 16-значную строку с ведущими нулями
        card_str = f"{number:016d}"
        # Разбиваем на группы по 4 символа
        yield f"{card_str[0:4]} {card_str[4:8]} {card_str[8:12]} {card_str[12:16]}"