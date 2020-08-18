from dataclasses import dataclass, field
from functools import reduce
from operator import add
from typing import List

from source.domain.models.salses.daily_sales import DailySales


@dataclass(frozen=True)
class ShopMonthlySales:
    shop_code: str
    year_month: str
    daily_sales_list: List[DailySales] = field(default_factory=list, compare=False)

    def amount(self) -> int:
        return reduce(add, map(lambda data: data.amount(), self.daily_sales_list))

