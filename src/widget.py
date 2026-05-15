from src.masks import get_mask_card_number, get_mask_account


def mask_account_card(input_string: str) -> str:
    """
    Маскирует номер карты или счёта.

    Args:
        input_string (str): Строка с типом и номером (например,
                           "Visa Platinum 7000792289606361" или
                           "Счет 73654108430135874305")

    Returns:
        str: Строка с замаскированным номером

    Examples:
        >>> mask_account_card("Visa Platinum 7000792289606361")
        'Visa Platinum 7000 79** **** 6361'

        >>> mask_account_card("Счет 73654108430135874305")
        'Счет **4305'
    """
    # Разделяем строку на части по пробелам
    parts = input_string.split()

    # Последняя часть - это номер (всегда)
    number = parts[-1]

    # Всё остальное - это тип (имя карты/счёта)
    card_type = " ".join(parts[:-1])

    # Определяем тип по длине номера:
    # Карта = 16 цифр, Счёт = 20 цифр
    if len(number) == 16:
        # Используем функцию маскировки карты
        masked_number = get_mask_card_number(number)
    elif len(number) == 20:
        # Используем функцию маскировки счёта
        masked_number = get_mask_account(number)
    else:
        raise ValueError(f"Неверная длина номера: {len(number)} (должно быть 16 или 20)")

    # Возвращаем тип + замаскированный номер
    return f"{card_type} {masked_number}"


