from typing import List

from source.domain.models.salses.shop_monthly_sales import ShopMonthlySales
from source.domain.repository.shop_sales_repository_base import ShopSalesRepositoryBase


class S3ShopSalesRepository(ShopSalesRepositoryBase):
    """
     S3での店舗売上レポジトリの実装
     """
    __bucket_name: str
    __file_key: str

    def __init__(self, bucket_name=None, file_key=None) -> None:
        self.__bucket_name = bucket_name
        self.__file_key = file_key
        if self.__bucket_name is None or self.__file_key is None:
            raise ValueError('bucket_nameとfile_keyを指定してください')

    def save(self, data: List[ShopMonthlySales]) -> None:
        pass