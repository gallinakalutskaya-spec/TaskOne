import pandas as pd
from typing import Any, Dict, List


def read_transactions_from_csv(file_path: str) -> List[Dict[str, Any]]:
    """
    Считывает финансовые операции из CSV-файла.

    :param file_path: Путь к файлу CSV.
    :return: Список словарей с транзакциями.
    """
    dataframe = pd.read_csv(file_path, delimiter=";")
    return dataframe.to_dict(orient="records")


def read_transactions_from_excel(file_path: str) -> List[Dict[str, Any]]:
    """
    Считывает финансовые операции из Excel-файла.

    :param file_path: Путь к файлу Excel.
    :return: Список словарей с транзакциями.
    """
    dataframe = pd.read_excel(file_path)
    return dataframe.to_dict(orient="records")
