def get_mask_card_number(card_number: str) -> str:
    """
    Маскирует номер банковской карты.
    Args:
        card_number (str): Номер карты (16 цифр).

    Returns
        str: Замаскированный номер в формате XXXX XX** **** XXXX
    """

    # Проверка: длина должна быть 16 символов
    if len(card_number) != 16 or not card_number.isdigit():
        raise ValueError(f"Номер карты должен содержать 16 цифр, а не {len(card_number)}")

    mask = f"{card_number[:4]} {card_number[4:6]}** **** {card_number[-4:]}"
    return mask


def get_mask_account(account_number: str) -> str:
    """
    Маскирует номер счёта.
    Принимает строку из 20 цифр, возвращает '**XXXX'.
    """
    # 🔒 Валидация: только цифры и ровно 20 символов
    if not account_number.isdigit() or len(account_number) != 20:
        raise ValueError("Номер счёта должен состоять из ровно 20 цифр")

    return f"**{account_number[-4:]}"