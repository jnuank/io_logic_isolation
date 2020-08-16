from source.domain.repository.code_repository_base import CodeRepositoryBase


class InMemoryCodeRepository(CodeRepositoryBase):
    """
    インメモリリポジトリ実装
    """

    def __init__(self):
        # key:外部システムの店舗コード value:店舗コード
        self.__shop_code_table = {
            '1': '001',
            '2': '002',
            '3': '003'
        }
        # key:(外部システム店舗コード, 外部システムレジ番号) value:レジ番号
        # レジ番号の頭1桁目が「0」:常設レジ、「9」:催事レジ
        self.__cash_register_code_table = {
            ('1', '1'): '001',
            ('1', '2'): '901',
            ('2', '1'): '001',
        }

    def get_shop_code(self, external_system_shop_code: str) -> str:
        """
        店舗コードを取得する
        :param external_system_shop_code: 外部システムで採番された店舗コード
        :return: 店舗コード
        """
        result = self.__shop_code_table.get(external_system_shop_code)
        if result is None:
            raise ValueError(f'指定したキーに該当する施設IDは存在しません。キー:{external_system_shop_code}')

        return result

    def get_cash_register_code(self, external_system_shop_code: str, external_system_cash_register_code:str) -> str:
        """
        レジ番号を取得する
        :param external_system_shop_code: 外部システムで採番された店舗コード
        :param external_system_cash_register_code: 外部システムで採番されたレジ番号
        :return: レジ番号
        """

        result = self.__cash_register_code_table.get((external_system_shop_code, external_system_cash_register_code))

        if result is None:
            raise ValueError(f'指定したキーに該当する入居者IDは存在しません。キー:{external_system_cash_register_code}')

        return result
