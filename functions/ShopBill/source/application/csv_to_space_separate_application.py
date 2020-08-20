import dataclasses

from source.domain.repository.csv_cash_transaction_repository_base import CsvCashTransactionRepositoryBase
from source.domain.rules.transfer_rules import TransferRules
from source.util.util import get_logger
from tests.In_memory_code_repository import InMemoryCodeRepository

logger = get_logger('INFO')

@dataclasses
class CsvToSpaceSeparateApplication(object):
    """
    CSV→スペース区切りに変換する処理
    """
    bucket: str
    key: str
    csv_repository: CsvCashTransactionRepositoryBase

    def csv_to_space_separate(self) -> None:
        """
        CSV→スペース区切り変換
        """

        # CSVモデルに変換
        csv_models = self.csv_repository.load()

        # ドメインモデルに変換
        shop_monthly_sales = TransferRules(InMemoryCodeRepository()).to_shop_sales(csv_models)

        # スペース区切りに変換して保存をする

