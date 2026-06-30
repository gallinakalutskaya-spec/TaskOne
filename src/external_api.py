"""Модуль для работы с внешними API."""

import os
from typing import Any

import requests
from dotenv import load_dotenv

# Загружаем переменные окружения из .env
load_dotenv()


def get_transaction_amount(transaction: dict[str, Any]) -> float:
    """
    Возвращает сумму транзакции в рублях (float).

    Если валюта USD или EUR, конвертирует через внешний API.

    Args:
        transaction: Словарь с данными о транзакции.

    Returns:
        Сумма транзакции в рублях.
    """
    operation_amount = transaction.get("operationAmount", {})
    amount_str = operation_amount.get("amount", "0")
    currency_info = operation_amount.get("currency", {})
    currency_code = currency_info.get("code", "RUB")

    amount = float(amount_str)

    # Если валюта не рубли, конвертируем
    if currency_code in ("USD", "EUR"):
        rate = get_exchange_rate(currency_code, "RUB")
        amount = amount * rate

    return amount


def get_exchange_rate(base_currency: str, target_currency: str) -> float:
    """
    Получает текущий курс валюты через Exchange Rates Data API.

    Args:
        base_currency: Код базовой валюты (например, "USD").
        target_currency: Код целевой валюты (например, "RUB").

    Returns:
        Курс валюты.
    """
    api_key = os.getenv("EXCHANGE_RATES_API_KEY")
    if not api_key:
        raise ValueError("API ключ не найден в переменных окружения")

    url = "http://api.exchangeratesapi.io/v1/latest"
    params = {
        "access_key": api_key,
        "base": base_currency,
        "symbols": target_currency
    }

    response = requests.get(url, params=params, timeout=10)
    response.raise_for_status()

    data = response.json()

    if "rates" not in data or target_currency not in data["rates"]:
        raise ValueError(f"Не удалось получить курс для {base_currency} -> {target_currency}")

    return float(data["rates"][target_currency])
