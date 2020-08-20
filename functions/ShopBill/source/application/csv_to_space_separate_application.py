from dataclasses import dataclass

from source.domain.repository.code_repository_base import CodeRepositoryBase
from source.domain.repository.csv_cash_transaction_repository_base import CsvCashTransactionRepositoryBase
from source.domain.repository.shop_sales_repository_base import ShopSalesRepositoryBase
from source.domain.rules.transfer_rules import TransferRules
from source.util.util import get_logger

logger = get_logger('INFO')


@dataclass
class CsvToSpaceSeparateApplication(object):
    """
    CSV→スペース区切りに変換する処理
    """
    code_repository: CodeRepositoryBase
    csv_repository: CsvCashTransactionRepositoryBase
    shop_sales_repository: ShopSalesRepositoryBase

    def csv_to_space_separate(self) -> None:
        """
        CSV→スペース区切り変換
        """

        # CSVモデルに変換
        csv_models = self.csv_repository.load()

        # ドメインモデルに変換
        shop_monthly_sales = TransferRules(self.code_repository).to_shop_sales(csv_models)

        # スペース区切りに変換して保存をする
        self.shop_sales_repository.save(shop_monthly_sales)
