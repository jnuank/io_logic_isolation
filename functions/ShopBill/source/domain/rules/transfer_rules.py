from dataclasses import dataclass
from datetime import datetime, date
from itertools import groupby
from typing import List

from source.domain.models.csv_models.csv_cash_transaction_header import CsvCashTransactionHeader
from source.domain.models.salses.daily_sales import DailySales
from source.domain.models.salses.daily_sales_detail import DailySalesDetail
from source.domain.models.salses.shop_monthly_sales import ShopMonthlySales
from source.domain.repository.code_repository_base import CodeRepositoryBase


@dataclass(frozen=True)
class TransferRules(object):
    """
    変換ルールクラス
    """
    repository: CodeRepositoryBase

    def to_shop_sales(self, sources: List[CsvCashTransactionHeader]) -> List[ShopMonthlySales]:
        results: List[ShopMonthlySales] = []

        sources.sort(key=lambda x: x.shop_code)

        # 店舗ごとにグルーピングをし、モデルに変換する
        for key, g in groupby(sources, key=lambda x: x.shop_code):
            shop_code = self.repository.get_shop_code(key)

            details: List[DailySalesDetail] = []
            dt = ''
            day = ''
            year_month = ''
            for member in g:
                dt = datetime.strptime(member.transaction_datetime, '%Y%m%d%H%M%S')
                day = date(dt.year, dt.month, dt.day)
                year_month = member.transaction_datetime[:6]

                cash_register_code = self.repository.get_cash_register_code(member.shop_code, member.cash_register_code)
                amount = sum([s.unit_price * s.quantity for s in member.transaction_details])

                detail = DailySalesDetail(member.transaction_code,
                                          dt,
                                          cash_register_code,
                                          amount)

                details.append(detail)

            daily = DailySales(day, details)
            shop_sales = ShopMonthlySales(shop_code, year_month, [daily])

            results.append(shop_sales)

        return results
