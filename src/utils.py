"""Модуль для работы с файлами данных."""

import json
import os
from typing import Any

from src.logger_config import setup_logger

# Создаём логгер для этого модуля
logger = setup_logger(
    logger_name=__name__,
    log_file="logs/utils.log"
)


def read_json_file(file_path: str) -> list[dict[str, Any]]:
    """
    Читает JSON-файл и возвращает список словарей с транзакциями.

    Args:
        file_path: Путь к JSON-файлу.

    Returns:
        Список словарей с данными о транзакциях.
        Пустой список, если файл пустой, содержит не список или не найден.
    """
    logger.info(f"Попытка чтения JSON-файла: {file_path}")

    try:
        # Проверяем существование файла
        if not os.path.exists(file_path):
            logger.warning(f"Файл не найден: {file_path}")
            return []

        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read().strip()

            # Проверяем, что файл не пустой
            if not content:
                logger.warning(f"Файл пустой: {file_path}")
                return []

            data = json.loads(content)

            # Проверяем, что данные - это список
            if not isinstance(data, list):
                logger.error(f"Данные в файле не являются списком: {file_path}")
                return []

            logger.info(f"Успешно прочитано {len(data)} записей из файла: {file_path}")
            return data

    except (json.JSONDecodeError, IOError, OSError) as e:
        logger.error(f"Ошибка при чтении файла {file_path}: {type(e).__name__}: {e}")
        return []