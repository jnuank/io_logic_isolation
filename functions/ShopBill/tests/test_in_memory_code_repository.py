from pytest import raises

from tests.in_memory_code_repository import InMemoryCodeRepository


class TestInMemoryCodeRepository:

    def test_店舗コード001が返る(self):
        result = InMemoryCodeRepository().get_shop_code('1')

        assert result == '001'

    def test_店舗コード003が返る(self):
        result = InMemoryCodeRepository().get_shop_code('3')

        assert result == '003'

    def test_レジ番号901が返る(self):
        result = InMemoryCodeRepository().get_cash_register_code('1', '2')

        assert result == '901'

    def test_存在しない店舗コードエラーが返る(self):
        with raises(ValueError):
            InMemoryCodeRepository().get_shop_code('999')

    def test_存在しないレジ番号エラーが返る(self):
        with raises(ValueError):
            InMemoryCodeRepository().get_cash_register_code('999', '111')

