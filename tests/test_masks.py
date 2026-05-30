import pytest

from src.masks import get_mask_card_number


@pytest.mark.parametrize(
    "card_number,expected",
    [("4545787845121258","4545 78** **** 1258")]
)
def test_get_mask_card_number(card_number,expected):
    assert get_mask_card_number (card_number) == expected

def test_get_mask_card_number_wrong():
    with pytest.raises(ValueError):
        get_mask_card_number("card")

def test_get_mask_account():
    pass
