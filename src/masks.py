def get_mask_card_number(card_number: str) -> str:
    """
    Маскирует номер банковской карты.
    Args:
        card_number (str): Номер карты (16 цифр).

    Returns
        str: Замаскированный номер в формате XXXX XX** **** XXXX
    """

    # Проверка: длина должна быть 16 символов
    if len(card_number) != 16:
        raise ValueError(f"Номер карты должен содержать 16 цифр, а не {len(card_number)}")

    mask = f"{card_number[:4]} {card_number[4:6]}** **** {card_number[-4:]}"
    return mask


def get_mask_account(account_number: str) -> str:
    """
    Маскирует номер банковского счета
    Args:
        account_number(str): Номер счета (20 цифр)
    Returns
        str: Замаскированный счет в формате **XXXX (видны последние 4 цифры)
    """
    # Проверка: длина должна быть 20 символов
    if len(account_number) != 20:
        raise ValueError(f"Номер счёта должен содержать 20 цифр, а не {len(account_number)}")

    mask = f"**{account_number[-4:]}"
    return mask
