import dataclasses
from typing import List

from source.domain.models.care_csv_bills.care_csv_basic_bill import CareCsvBasicBill
from source.domain.repository.care_bill_repository_base import CareBillRepositoryBase
from source.domain.repository.care_csv_bill_repository_base import CareCsvBillRepositoryBase
from source.domain.repository.code_repository_base import CodeRepositoryBase
from source.domain.rules.csv_to_pompa import TransferRules
from source.util.util import get_logger

logger = get_logger('INFO')

@dataclasses
class CsvToSpaceSeparateApplication(object):
    """
    CSV→スペース区切りに変換する処理
    """
    bucket: str
    key: str

    def csv_to_space_separate(self) -> None:
        """
        CSV→スペース区切り変換
        """
        pass