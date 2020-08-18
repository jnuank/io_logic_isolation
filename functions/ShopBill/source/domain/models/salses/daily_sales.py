from dataclasses import dataclass, field
from datetime import datetime
from functools import reduce
from operator import add
from typing import List

from source.domain.models.salses.daily_sales_detail import DailySalesDetail


@dataclass(frozen=True)
class DailySales:
    sales_date: datetime.date
    details: List[DailySalesDetail] = field(default_factory=list, compare=False)

    def amount(self) -> int:
        return reduce(add, map(lambda data: data.amount, self.details))
