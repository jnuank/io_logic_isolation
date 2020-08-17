from dataclasses import dataclass


@dataclass(frozen=True)
class CsvCashTransactionDetail:
    """
    レジ取引データ明細CSVのモデル
    """
    # 商品名
    item_name: str
    # 単価
    unit_price: int
    # 数量
    quantity: int
