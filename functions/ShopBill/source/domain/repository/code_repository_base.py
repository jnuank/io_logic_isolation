from abc import ABCMeta, abstractmethod


class CodeRepositoryBase(object, metaclass=ABCMeta):
    """
    コードをデータストアから取得する抽象クラス
    """

    @abstractmethod
    def get_shop_code(self, external_system_shop_code: str) -> str:
        """
        店舗コードを取得する
        :param external_system_shop_code: 外部システムで採番された店舗コード
        :return: 店舗コード
        """
        raise NotImplementedError()

    @abstractmethod
    def get_cash_register_code(self, external_system_shop_code: str, external_system_cash_register_code: str) -> str:
        """
        レジ番号を取得する
        :param external_system_shop_code: 外部システムで採番された店舗コード
        :param external_system_cash_register_code: 外部システムで採番されたレジ番号
        :return: レジ番号
        """
        raise NotImplementedError()