"""Модуль с декораторами для логирования."""

import functools
from typing import Any, Callable, Optional


def log(filename: Optional[str] = None) -> Callable:
    """
    Декоратор для логирования вызовов функций.

    Записывает успешные результаты или ошибки в файл или консоль.

    Args:
        filename: Путь к файлу для записи логов. Если None, вывод идет в консоль.

    Returns:
        Декорированная функция.
    """

    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            log_message = ""
            try:
                # Пытаемся выполнить функцию
                result = func(*args, **kwargs)
                log_message = (
                    f"Вызов функции {func.__name__} завершился успешно. "
                    f"Результат: {result}"
                )
                return result
            except Exception as e:
                # Если произошла ошибка, формируем сообщение о ней
                log_message = (
                    f"Вызов функции {func.__name__} завершился с ошибкой. "
                    f"Тип ошибки: {type(e).__name__}. "
                    f"Входные параметры: args={args}, kwargs={kwargs}"
                )
                raise  # Обязательно пробрасываем ошибку дальше
            finally:
                # Логируем в зависимости от наличия filename
                if filename:
                    with open(filename, "a", encoding="utf-8") as f:
                        f.write(log_message + "\n")
                else:
                    print(log_message)

        return wrapper

    return decorator

