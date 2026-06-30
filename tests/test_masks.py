import pytest

from src.masks import get_mask_card_number, get_mask_account


@pytest.mark.parametrize(
    "card_number,expected",
    [("4545787845121258","4545 78** **** 1258"),
     ("7000792289606361", "7000 79** **** 6361"),
     ("0000000000000000", "0000 00** **** 0000"),
])
def test_get_mask_card_number(card_number,expected):
    """Проверка корректного маскирования валидных номеров карт"""
    assert get_mask_card_number (card_number) == expected

@pytest.mark.parametrize("wrong_card", [
    '',
    "123",
    "12345678901234567",
    "card_number",
    "454578784512125a",
    "4545 7878 4512 1258",
])
def test_get_mask_card_number_wrong(wrong_card):
    with pytest.raises(ValueError):
        get_mask_card_number(wrong_card)


@pytest.mark.parametrize("account,expected", [
    ("45254655214656512655","**2655"),
    ("73654108430135874305", "**4305"),
    ("00000000000000000001", "**0001"),
])
def test_get_mask_account_parametrize(account,expected):
    assert get_mask_account(account) == expected


@pytest.mark.parametrize("invalid_account", [
    "",
    "123",
    "1234567890123456789",
    "123456789012345678901",
    "account_123",
    "4525465521465651265a",
])
def test_get_mask_account_invalid(invalid_account):
    """Проверка обработки некорректных вводов для счетов."""
    with pytest.raises(ValueError):
        get_mask_account(invalid_account)