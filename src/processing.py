from typing import Any

def filter_by_state(data: list[dict], state: str = "EXECUTED") -> list[dict]:
    """
    Фильтрует список словарей по значению ключа state.

    Args:
        data: Список словарей.
        state: Значение для фильтрации (по умолчанию "EXECUTED").

    Returns:
        Новый список словарей, соответствующих условию.
    """
    result = []
    for item in data:
        if item.get("state") == state:
            result.append(item)
    return result


def sort_by_date(data: list[dict], reverse: bool = True) -> list[dict]:
    """
    Сортирует список словарей по дате.

    Args:
        data: Список словарей с ключом 'date'.
        reverse: Порядок сортировки (True - убывание, False - возрастание).

    Returns:
        Новый отсортированный список.
    """
    return sorted(data, key=lambda x: x["date"], reverse=reverse)
