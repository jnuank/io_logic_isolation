from __future__ import annotations

from dataclasses import dataclass, field
from typing import List

from source.domain.models.csv_models.csv_cash_transaction_detail import CsvCashTransactionDetail


@dataclass(frozen=True, order=True)
class CsvCashTransactionHeader:
    """
    レジ取引データCSVのモデル
    """
    # 店舗コード
    shop_code: str = field(compare=True)
    # レジ番号
    cash_register_code: str = field(compare=True)
    # 取引番号
    transaction_code: str = field(compare=True)
    # 取引時刻
    transaction_datetime: str = field(compare=True)
    # 取引明細
    transaction_details: List[CsvCashTransactionDetail]