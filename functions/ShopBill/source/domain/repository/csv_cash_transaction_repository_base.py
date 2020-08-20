from abc import ABCMeta, abstractmethod
from typing import List

from source.domain.models.csv_models.csv_cash_transaction_header import CsvCashTransactionHeader


class CsvCashTransactionRepositoryBase(object, metaclass=ABCMeta):
    """
    CSVのレジ取引データを受け取るためのRepository抽象クラス
    """

    @abstractmethod
    def load(self) -> List[CsvCashTransactionHeader]:
        """
        レジ取引データモデルを取得する
        :param file_path: csvファイルパス
        :return: レジ取引データモデル
        """
        raise NotImplementedError()

    @abstractmethod
    def save(self, data: CsvCashTransactionHeader) -> None:
        """
        レジ取引データモデルを保存する
        :param data: レジ取引データモデル
        """
        raise NotImplementedError('まだSaveできません')
