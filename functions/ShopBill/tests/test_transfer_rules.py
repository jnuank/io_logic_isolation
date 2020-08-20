from source.domain.models.csv_models.csv_cash_transaction_header import CsvCashTransactionHeader
from source.domain.rules.transfer_rules import TransferRules
from tests.In_memory_code_repository import InMemoryCodeRepository


class TestTransferRules:

    def test_Csvモデル渡したらドメインモデルになる(self):

        csv_models = CsvCashTransactionHeader.from_csv('cash_register.csv')

        results = TransferRules(InMemoryCodeRepository()).to_shop_sales(csv_models)

        assert results[0].shop_code == '001'
        assert results[0].year_month == '202008'
        assert results[0].amount() == 22000
