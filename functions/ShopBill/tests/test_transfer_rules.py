from source.domain.models.csv_models.csv_cash_transaction_header import CsvCashTransactionHeader
from source.domain.rules.transfer_rules import TransferRules
from tests.In_memory_code_repository import InMemoryCodeRepository


class TestTransferRules:

    def test_Csvモデル渡したらドメインモデルになる(self):

        csv_models = CsvCashTransactionHeader.from_csv('cash_register.csv')

        shop_monthly_sales = TransferRules(InMemoryCodeRepository()).to_shop_sales(csv_models)

        assert shop_monthly_sales[0].shop_code == '001'
        assert shop_monthly_sales[0].year_month == '202008'
        assert shop_monthly_sales[0].amount() == 51300

        assert shop_monthly_sales[1].shop_code == '002'
        assert shop_monthly_sales[1].year_month == '202008'
        assert shop_monthly_sales[1].amount() == 4900
