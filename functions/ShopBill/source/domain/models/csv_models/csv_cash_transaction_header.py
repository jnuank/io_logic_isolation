from dataclasses import dataclass
from typing import List

from source.domain.models.csv_models.csv_cash_transaction_detail import CsvCashTransactionDetail


@dataclass(frozen=True)
class CsvCashTransactionHeader:
    """
    レジ取引データCSVのモデル
    """
    # 店舗コード
    shop_code: str
    # レジ番号
    cash_register_code: str
    # 取引番号
    transaction_code: str
    # 取引時刻
    transaction_datetime: str
    # 取引明細
    transaction_details: List[CsvCashTransactionDetail]