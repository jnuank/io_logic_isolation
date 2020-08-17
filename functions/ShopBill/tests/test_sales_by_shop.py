from dataclasses import dataclass
from typing import List

import pandas as pd

from source.domain.repository.code_repository_base import CodeRepositoryBase
from tests.In_memory_code_repository import InMemoryCodeRepository


@dataclass
class CsvToShopSales:
    code_respository: CodeRepositoryBase

    def csv_to_sales_by_shop(self, csv_list) -> List[List[str]]:
        names_list = list(range(10))
        df = pd.read_csv(csv_list, names=names_list, dtype='object').fillna('_')

        SHOP_COLUMN = 0
        # 店舗コードでグルーピングする
        shop_group_list = df.groupby([SHOP_COLUMN, 1, 3])

        results = []
        for group_rows in shop_group_list:
            print(group_rows[0][0])

            shop_code = self.code_respository.get_shop_code(group_rows[0])
            year_month = [record[4] for record in group_rows[1].values.tolist() if record[2] == '01'][0][:6]
            amount_list = [int(record[5]) * int(record[6]) for record in group_rows[1].values.tolist() if record[2] == '02']
            sales_amount = sum(amount_list)

            results.append([shop_code, year_month, str(sales_amount)])

        return results


class TestSalesByShop:

    def test_変換がされること(self):

        results = CsvToShopSales(InMemoryCodeRepository()).csv_to_sales_by_shop('cash_register.csv')

        assert results[0][2] == '51300'
