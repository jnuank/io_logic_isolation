from abc import ABCMeta, abstractmethod
from typing import List

from source.domain.models.salses.shop_monthly_sales import ShopMonthlySales


class ShopSalesRepositoryBase(object, metaclass=ABCMeta):
    """
    店舗売上のRepository抽象クラス
    """

    @abstractmethod
    def load(self) -> List[ShopMonthlySales]:
        """
        店舗売上を取得する
        :return: 店舗売上
        """
        raise NotImplementedError(f'未実装エラー:{self.__class__.__name__}')

    @abstractmethod
    def save(self, sources: List[ShopMonthlySales]) -> None:
        """
        店舗売上を保存する
        :param data: 店舗売上
        """
        raise NotImplementedError(f'未実装エラー:{self.__class__.__name__}')
