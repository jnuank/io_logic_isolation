from typing import List

import pandas as pd
from source.domain.models.care_csv_bills.care_csv_total_bill import CareCsvTotalBill
from source.domain.models.care_csv_bills.csv_cash_transaction_detail import CareCsvDetailBill
from source.domain.models.care_csv_bills.csv_cash_transaction_header import CsvCashTransaction

from source.domain.repository.csv_cash_transaction_repository_base import CareCsvBillRepositoryBase


class MockCareCsvBillRepositoryFujiData(CareCsvBillRepositoryBase):
    """
    介護請求CSV、明細がない場合
    """
    __bucket_name: str
    __file_key: str

    def __init__(self, bucket_name=None, file_key=None) -> None:
        self.__bucket_name = bucket_name
        self.__file_key = file_key
        if self.__bucket_name is None or self.__file_key is None:
            raise Exception('bucket_nameとfile_keyを指定してください')

    def get(self) -> List[CsvCashTransaction]:
        """
        介護請求情報を取得する
        :return: 介護請求
        """

        # 欠損値(nan)をアンダースコアに変換する(ユニケージ用への変換)
        # encoding='cp932'指定しているのは、こちら参照　https://qiita.com/tackey/items/5b7b2be23af60335fe11
        # Lambdaの載せる方の本番コードの方では、とくに指定がいらなかった
        # Lambda上で動くAmazon LinuxOSの関係？
        names_list = list(range(30))
        df = pd.read_csv(
            self.__file_key,
            names=names_list,
            dtype='object').fillna('_')

        INSURED_NUMBER_COLUMN = 3

        # 被保険者番号でグルーピングする
        # この時、ヘッダや集計行を省くため、被保険者番号列で数字のみで抽出
        insured_group_list = df[df[INSURED_NUMBER_COLUMN].str.contains(
            '[0-9]')].groupby(INSURED_NUMBER_COLUMN)

        basics: List[CsvCashTransaction] = []

        for row in insured_group_list:
            totals: List[CareCsvTotalBill] = []
            details: List[CareCsvDetailBill] = []

            office_number: str
            insured_number: str

            # CSVデータからモデルを生成する
            # 不要な空白が入っているため、strip()で除去
            for row2 in row[1].values.tolist():

                split_date = row2[8].split('/')
                year_month = split_date[0] + split_date[1]
                total_model = CareCsvTotalBill(year_month,
                                               row2[20].strip(),
                                               row2[19].strip(),
                                               )

                totals.append(total_model)

                office_number = row2[9].strip()
                insured_number = row2[3].strip()

            model = CsvCashTransaction(office_number,
                                       insured_number,
                                       details,
                                       totals)

            basics.append(model)

        return basics

    def save(self, data: CsvCashTransaction) -> None:
        """
        介護請求情報を保存する
        :param data: 介護請求
        """
        raise NotImplementedError('まだ未実装です')
