"""Модуль для работы с файлами данных."""

import json
import os
from typing import Any


def read_json_file(file_path: str) -> list[dict[str, Any]]:
    """
    Читает JSON-файл и возвращает список словарей с транзакциями.

    Args:
        file_path: Путь к JSON-файлу.

    Returns:
        Список словарей с данными о транзакциях.
        Пустой список, если файл пустой, содержит не список или не найден.
    """
    try:
        # Проверяем существование файла
        if not os.path.exists(file_path):
            return []

        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read().strip()

            # Проверяем, что файл не пустой
            if not content:
                return []

            data = json.loads(content)

            # Проверяем, что данные - это список
            if not isinstance(data, list):
                return []

            return data

    except (json.JSONDecodeError, IOError, OSError):
        # Любая ошибка чтения или парсинга JSON
        return []
