import unittest
from unittest.mock import MagicMock, patch

import pandas as pd

from external_sources import (
    read_transactions_from_csv,
    read_transactions_from_excel,
)


class TestExternalSources(unittest.TestCase):
    """Тесты для модуля external_sources."""

    @patch("external_sources.pd.read_csv")
    def test_read_transactions_from_csv(self, mock_read_csv: MagicMock) -> None:
        """Тест считывания транзакций из CSV-файла."""
        mock_df = MagicMock(spec=pd.DataFrame)
        mock_df.to_dict.return_value = [{"id": 650703, "state": "EXECUTED"}]
        mock_read_csv.return_value = mock_df

        result = read_transactions_from_csv("transactions.csv")

        mock_read_csv.assert_called_once_with("transactions.csv", delimiter=";")
        mock_df.to_dict.assert_called_once_with(orient="records")
        self.assertEqual(result, [{"id": 650703, "state": "EXECUTED"}])

    @patch("external_sources.pd.read_excel")
    def test_read_transactions_from_excel(
        self, mock_read_excel: MagicMock
    ) -> None:
        """Тест считывания транзакций из Excel-файла."""
        mock_df = MagicMock(spec=pd.DataFrame)
        mock_df.to_dict.return_value = [{"id": 650703, "state": "EXECUTED"}]
        mock_read_excel.return_value = mock_df

        result = read_transactions_from_excel("transactions_excel.xlsx")

        mock_read_excel.assert_called_once_with("transactions_excel.xlsx")
        mock_df.to_dict.assert_called_once_with(orient="records")
        self.assertEqual(result, [{"id": 650703, "state": "EXECUTED"}])


if __name__ == "__main__":
    unittest.main()
