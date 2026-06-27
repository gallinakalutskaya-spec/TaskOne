"""Тесты для модуля utils."""

import json
import os
import tempfile
from src.utils import read_json_file


def test_read_json_file_success():
    """Тест успешного чтения валидного JSON-файла."""
    test_data = [{"id": 1, "amount": "100"}]

    with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as f:
        json.dump(test_data, f)
        temp_path = f.name

    try:
        result = read_json_file(temp_path)
        assert result == test_data
    finally:
        os.remove(temp_path)


def test_read_json_file_not_found():
    """Тест: файл не найден."""
    result = read_json_file("nonexistent_file.json")
    assert result == []


def test_read_json_file_empty():
    """Тест: пустой файл."""
    with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as f:
        temp_path = f.name

    try:
        result = read_json_file(temp_path)
        assert result == []
    finally:
        os.remove(temp_path)


def test_read_json_file_not_list():
    """Тест: файл содержит не список (например, словарь)."""
    test_data = {"key": "value"}

    with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as f:
        json.dump(test_data, f)
        temp_path = f.name

    try:
        result = read_json_file(temp_path)
        assert result == []
    finally:
        os.remove(temp_path)


def test_read_json_file_invalid_json():
    """Тест: файл содержит невалидный JSON."""
    with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as f:
        f.write("invalid json content")
        temp_path = f.name

    try:
        result = read_json_file(temp_path)
        assert result == []
    finally:
        os.remove(temp_path)