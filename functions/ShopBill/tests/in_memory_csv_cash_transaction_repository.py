from dataclasses import dataclass
from typing import List

import pandas as pd

from source.domain.models.csv_models.csv_cash_transaction_detail import CsvCashTransactionDetail
from source.domain.models.csv_models.csv_cash_transaction_header import CsvCashTransactionHeader
from source.domain.repository.csv_cash_transaction_repository_base import CsvCashTransactionRepositoryBase


@dataclass
class InMemoryCsvCashTransactionRepository(CsvCashTransactionRepositoryBase):
    """
    CSVモデルインメモリリポジトリ実装
    """

    def save(self, data: CsvCashTransactionHeader) -> None:
        pass

    file_path: str

    def load(self) -> List[CsvCashTransactionHeader]:
        names_list = list(range(10))
        df = pd.read_csv(self.file_path, names=names_list, dtype='object').fillna('_')

        SHOP_COLUMN = 0
        CASH_REJISTER_COLUMN = 1
        TRANSACTION_COLUMN = 3

        shop_group_list = df.groupby([SHOP_COLUMN, CASH_REJISTER_COLUMN, TRANSACTION_COLUMN])

        results = []
        for group_rows in shop_group_list:
            shop_code = group_rows[0][0]
            cash_register_code = group_rows[0][1]
            transaction_code = group_rows[0][2]
            year_month = [r[4] for r in group_rows[1].values.tolist() if r[2] == '01'][0]

            details = []
            for detail_row in group_rows[1].values.tolist():
                if detail_row[2] == '01':
                    continue

                detail = CsvCashTransactionDetail(detail_row[4], int(detail_row[5]), int(detail_row[6]))
                details.append(detail)

            header = CsvCashTransactionHeader(shop_code, cash_register_code, transaction_code, year_month, details)

            results.append(header)

        return results

