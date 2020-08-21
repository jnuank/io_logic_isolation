from typing import List

import boto3

from source.domain.models.salses.shop_monthly_sales import ShopMonthlySales
from source.domain.repository.shop_sales_repository_base import ShopSalesRepositoryBase


class S3ShopSalesRepository(ShopSalesRepositoryBase):
    """
     インメモリでの店舗売上レポジトリの実装
     """
    __bucket_name: str

    def __init__(self, bucket_name):
        self.__bucket_name = bucket_name

    def save(self, sources: List[ShopMonthlySales]) -> None:
        self.shop_monthly_sales = []
        self.daily_sales = []
        self.daily_details = []
        for source in sources:
            self.shop_monthly_sales.append(
                [source.shop_code, source.year_month, str(source.amount())]
            )
            for daily in source.daily_sales_list:
                self.daily_sales.append([
                    source.shop_code,
                    daily.sales_date.strftime('%Y%m%d'),
                    str(daily.amount()),
                ])

                for detail in daily.details:
                    self.daily_details.append(
                        [source.shop_code,
                         detail.transaction_code,
                         detail.cash_number,
                         detail.transaction_datetime.strftime('%Y%m%d%H%M%S'),
                         str(detail.amount)]
                    )

        self.shop_monthly_sales = self.__comma2dlist_to_space2dlist(self.shop_monthly_sales)
        self.daily_sales = self.__comma2dlist_to_space2dlist(self.daily_sales)
        self.daily_details = self.__comma2dlist_to_space2dlist(self.daily_details)

        try:
            self.__s3_upload(self.shop_monthly_sales, self.__bucket_name, '店舗売上.txt')
            self.__s3_upload(self.daily_details, self.__bucket_name, '店舗日別.txt')
            self.__s3_upload(self.daily_details, self.__bucket_name, '店舗日別詳細.txt')
        except Exception as error:
            raise error

    def __s3_upload(self, upload_list, bucket_name, upload_key):
        write_file = '/tmp/upload_text'
        s3 = boto3.resource('s3')
        f = open(write_file, 'w')  # 書き込みモードで開く
        f.write(upload_list)  # 引数の文字列をファイルに書き込む
        f.close()

        upload_bucket = s3.Bucket(bucket_name)
        upload_bucket.upload_file(write_file, upload_key)

    def __comma2dlist_to_space2dlist(self, csv_list) -> str:
        # すべての要素を文字列に変換
        str_2d_list = list(
            map(lambda x: list(map(lambda y: str(y), x)), csv_list))
        # スペース区切りに変換
        spaceDelimited = list(map(lambda x: " ".join(x), str_2d_list))
        test = "\n".join(spaceDelimited)

        print(test)
        return test + '\n'

    def load(self) -> List[ShopMonthlySales]:
        return super().load()