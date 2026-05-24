
def filter_by_state(date, state:str = "EXECUTED"):
    """
    Фильтрует список словарей по значению ключа state.

    Args:
        data: Список словарей.
        state: Значение для фильтрации (по умолчанию "EXECUTED").

    Returns:
        Новый список словарей, соответствующих условию.
    """
    result = []
    for item in date:
        if item["state"] == state:
            result.append(item)
    return result

def sort_by_date(data, reverse=True):
    """Сортирует список словарей по дате."""
    return sorted(data, key=lambda x: x["date"], reverse=reverse)