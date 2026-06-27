"""Тесты для модуля external_api."""

from unittest.mock import patch, Mock
import pytest
from src.external_api import get_transaction_amount, get_exchange_rate


def test_get_transaction_amount_rub():
    """Тест: транзакция в рублях (без конвертации)."""
    transaction = {
        "operationAmount": {
            "amount": "1000.50",
            "currency": {"code": "RUB"}
        }
    }

    result = get_transaction_amount(transaction)
    assert result == 1000.50


@patch("src.external_api.get_exchange_rate")
def test_get_transaction_amount_usd(mock_get_rate):
    """Тест: транзакция в USD (с конвертацией через API)."""
    mock_get_rate.return_value = 75.5  # Курс USD к RUB

    transaction = {
        "operationAmount": {
            "amount": "100.00",
            "currency": {"code": "USD"}
        }
    }

    result = get_transaction_amount(transaction)
    assert result == 7550.0  # 100 * 75.5
    mock_get_rate.assert_called_once_with("USD", "RUB")


@patch("src.external_api.get_exchange_rate")
def test_get_transaction_amount_eur(mock_get_rate):
    """Тест: транзакция в EUR (с конвертацией через API)."""
    mock_get_rate.return_value = 90.2  # Курс EUR к RUB

    transaction = {
        "operationAmount": {
            "amount": "50.00",
            "currency": {"code": "EUR"}
        }
    }

    result = get_transaction_amount(transaction)
    assert result == 4510.0  # 50 * 90.2
    mock_get_rate.assert_called_once_with("EUR", "RUB")


@patch("src.external_api.requests.get")
def test_get_exchange_rate_success(mock_get):
    """Тест успешного получения курса валюты."""
    mock_response = Mock()
    mock_response.json.return_value = {
        "rates": {"RUB": 75.5}
    }
    mock_response.raise_for_status = Mock()
    mock_get.return_value = mock_response

    result = get_exchange_rate("USD", "RUB")
    assert result == 75.5


@patch("src.external_api.requests.get")
def test_get_exchange_rate_api_error(mock_get):
    """Тест обработки ошибки API."""
    mock_response = Mock()
    mock_response.json.return_value = {"error": "Invalid API key"}
    mock_response.raise_for_status = Mock()
    mock_get.return_value = mock_response

    with pytest.raises(ValueError):
        get_exchange_rate("USD", "RUB")


@patch.dict("os.environ", {"EXCHANGE_RATES_API_KEY": ""})
def test_get_exchange_rate_missing_api_key():
    """Тест отсутствия API ключа."""
    with pytest.raises(ValueError, match="API ключ не найден"):
        get_exchange_rate("USD", "RUB")
