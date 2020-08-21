from dataclasses import dataclass, field
from typing import List

from source.domain.models.salses.shop_monthly_sales import ShopMonthlySales
from source.domain.repository.shop_sales_repository_base import ShopSalesRepositoryBase


@dataclass
class InMemoryShopSalesRepository(ShopSalesRepositoryBase):
    """
     インメモリでの店舗売上レポジトリの実装
     """
    shop_monthly_sales: List = field(init=False, default=list)
    daily_sales: List = field(init=False, default=list)
    daily_details: List = field(init=False, default=list)

    def save(self, sources: List[ShopMonthlySales]) -> None:
        self.shop_monthly_sales = []
        self.daily_sales = []
        self.daily_details = []
        for source in sources:
            self.shop_monthly_sales.append(
                [source.shop_code, source.year_month, str(source.amount())]
            )
            for daily in source.daily_sales_list:
                self.daily_sales.append([
                    source.shop_code,
                    daily.sales_date.strftime('%Y%m%d'),
                    str(daily.amount()),
                ])

                for detail in daily.details:
                    self.daily_details.append(
                        [source.shop_code,
                         detail.transaction_code,
                         detail.cash_number,
                         detail.transaction_datetime.strftime('%Y%m%d%H%M%S'),
                         str(detail.amount)]
                    )


        self.shop_monthly_sales = self.__comma2dlist_to_space2dlist(self.shop_monthly_sales)
        self.daily_sales = self.__comma2dlist_to_space2dlist(self.daily_sales)
        self.daily_details = self.__comma2dlist_to_space2dlist(self.daily_details)

    def __comma2dlist_to_space2dlist(self, csv_list) -> str:
        # すべての要素を文字列に変換
        str_2d_list = list(
            map(lambda x: list(map(lambda y: str(y), x)), csv_list))
        # スペース区切りに変換
        spaceDelimited = list(map(lambda x: " ".join(x), str_2d_list))
        test = "\n".join(spaceDelimited)

        print(test)
        return test + '\n'

    def load(self) -> List[ShopMonthlySales]:
        return super().load()