"""Модуль для маскировки номеров банковских карт и счетов."""

from src.logger_config import setup_logger

# Создаём логгер для этого модуля
logger = setup_logger(
    logger_name=__name__,
    log_file="logs/masks.log"
)


def get_mask_card_number(card_number: str) -> str:
    """Маскирует номер банковской карты (16 цифр)."""
    logger.info(f"Попытка маскировки номера карты: {card_number}")

    if not card_number.isdigit() or len(card_number) != 16:
        logger.error(f"Некорректный номер карты: {card_number}")
        raise ValueError("Номер карты должен состоять из ровно 16 цифр")

    masked = f"{card_number[:4]} {card_number[4:6]}** **** {card_number[-4:]}"
    logger.info(f"Номер карты успешно замаскирован: {masked}")
    return masked


def get_mask_account(account_number: str) -> str:
    """Маскирует номер счёта (20 цифр)."""
    logger.info(f"Попытка маскировки номера счёта: {account_number}")

    if not account_number.isdigit() or len(account_number) != 20:
        logger.error(f"Некорректный номер счёта: {account_number}")
        raise ValueError("Номер счёта должен состоять из ровно 20 цифр")

    masked = f"**{account_number[-4:]}"
    logger.info(f"Номер счёта успешно замаскирован: {masked}")
    return masked