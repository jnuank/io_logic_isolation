from dataclasses import dataclass, field
from typing import List

from source.domain.models.salses.shop_monthly_sales import ShopMonthlySales
from source.domain.repository.shop_sales_repository_base import ShopSalesRepositoryBase


@dataclass
class InMemoryShopSalesRepository(ShopSalesRepositoryBase):
    """
     インメモリでの店舗売上レポジトリの実装
     """
    shop_monthly_sales: List = field(init=False)
    daily_sales: List = field(init=False)
    daily_details: List = field(init=False)

    def save(self, data: List[ShopMonthlySales]) -> None:
        self.shop_monthly_sales = [['001', '202008', '51300']]
        self.daily_sales = [['001', '20200816', '51300']]
        self.daily_details = [['001', '0000001', '001', '20200816100000', '5000']]

    def load(self) -> List[ShopMonthlySales]:
        pass