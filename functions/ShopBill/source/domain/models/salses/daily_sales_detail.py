import datetime
from dataclasses import dataclass


@dataclass(frozen=True)
class DailySalesDetail:
    transaction_code: str
    transaction_datetime: datetime.datetime
    cash_number: str
    amount: int

