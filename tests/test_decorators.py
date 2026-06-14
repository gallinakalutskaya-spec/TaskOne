"""Тесты для модуля decorators."""

import os
import pytest
from src.decorators import log


# --- Вспомогательные функции для тестирования ---

@log()
def add_numbers(a: int, b: int) -> int:
    return a + b


@log(filename="test_success.log")
def multiply_numbers(a: int, b: int) -> int:
    return a * b


@log()
def divide_numbers(a: int, b: int) -> float:
    return a / b


@log(filename="test_error.log")
def subtract_numbers(a: int, b: int) -> int:
    return a - b


# --- Тесты ---

def test_log_success_console(capsys: pytest.CaptureFixture[str]) -> None:
    """Проверяет логирование успешного выполнения в консоль."""
    result = add_numbers(2, 3)

    assert result == 5
    captured = capsys.readouterr()
    assert "add_numbers" in captured.out
    assert "успешно" in captured.out
    assert "5" in captured.out


def test_log_success_file() -> None:
    """Проверяет логирование успешного выполнения в файл."""
    result = multiply_numbers(4, 5)

    assert result == 20
    assert os.path.exists("test_success.log")

    with open("test_success.log", "r", encoding="utf-8") as f:
        content = f.read()

    assert "multiply_numbers" in content
    assert "20" in content

    # Очистка после теста
    os.remove("test_success.log")


def test_log_error_console(capsys: pytest.CaptureFixture[str]) -> None:
    """Проверяет логирование ошибки в консоль."""
    with pytest.raises(ZeroDivisionError):
        divide_numbers(10, 0)

    captured = capsys.readouterr()
    assert "divide_numbers" in captured.out
    assert "ошибкой" in captured.out
    assert "ZeroDivisionError" in captured.out
    assert "args=(10, 0)" in captured.out
    assert "kwargs={}" in captured.out


def test_log_error_file() -> None:
    """Проверяет логирование ошибки в файл."""
    with pytest.raises(TypeError):
        # Специально передаем строку, чтобы вызвать TypeError при вычитании
        subtract_numbers("10", 5)  # type: ignore

    assert os.path.exists("test_error.log")

    with open("test_error.log", "r", encoding="utf-8") as f:
        content = f.read()

    assert "subtract_numbers" in content
    assert "TypeError" in content
    assert "args=('10', 5)" in content

    # Очистка после теста
    os.remove("test_error.log")
