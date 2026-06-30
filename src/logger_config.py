"""Модуль для настройки логгеров проекта."""

import logging
import os
from typing import Optional


def setup_logger(
        logger_name: str,
        log_file: Optional[str] = None,
        level: int = logging.DEBUG
) -> logging.Logger:
    """
    Настраивает и возвращает логгер.

    Args:
        logger_name: Имя логгера (обычно __name__ модуля).
        log_file: Путь к файлу лога. Если None, логи только в консоль.
        level: Уровень логирования (DEBUG, INFO, WARNING, ERROR, CRITICAL).

    Returns:
        Настроенный логгер.
    """
    logger = logging.getLogger(logger_name)
    logger.setLevel(level)

    # Очищаем старые обработчики (чтобы не дублировались при повторных вызовах)
    if logger.handlers:
        logger.handlers.clear()

    # Формат сообщения: время - модуль - уровень - сообщение
    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )

    # Обработчик для записи в файл (режим 'w' - перезапись)
    if log_file:
        # Создаём папку logs/, если её нет
        log_dir = os.path.dirname(log_file)
        if log_dir and not os.path.exists(log_dir):
            os.makedirs(log_dir)

        file_handler = logging.FileHandler(log_file, mode="w", encoding="utf-8")
        file_handler.setLevel(level)
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

    # Обработчик для вывода в консоль
    console_handler = logging.StreamHandler()
    console_handler.setLevel(level)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    return logger
