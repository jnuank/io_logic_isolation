from source.domain.rules.transfer_rules import TransferRules
from tests.In_memory_code_repository import InMemoryCodeRepository
from tests.in_memory_csv_cash_transaction_repository import InMemoryCsvCashTransactionRepository
from tests.in_memory_shop_sales_repository import InMemoryShopSalesRepository


class TestTransferRules:

    def test_Csvモデル渡したらドメインモデルになる(self):

        csv_models = InMemoryCsvCashTransactionRepository('cash_register.csv').load()

        shop_monthly_sales = TransferRules(InMemoryCodeRepository()).to_shop_sales(csv_models)

        assert shop_monthly_sales[0].shop_code == '001'
        assert shop_monthly_sales[0].year_month == '202008'
        assert shop_monthly_sales[0].amount() == 51300

        assert shop_monthly_sales[1].shop_code == '002'
        assert shop_monthly_sales[1].year_month == '202008'
        assert shop_monthly_sales[1].amount() == 4900

    def test_InMemory保存(self):
        csv_models = InMemoryCsvCashTransactionRepository('cash_register.csv').load()

        shop_monthly_sales = TransferRules(InMemoryCodeRepository()).to_shop_sales(csv_models)

        repository = InMemoryShopSalesRepository()
        repository.save(shop_monthly_sales)

        assert repository.shop_monthly_sales[0][0] == '001'
        assert repository.shop_monthly_sales[0][1] == '202008'
        assert repository.shop_monthly_sales[0][2] == '51300'

        assert repository.daily_sales[0][0] == '001'
        assert repository.daily_sales[0][1] == '20200816'
        assert repository.daily_sales[0][2] == '51300'

        assert repository.daily_details[0][0] == '001'
        assert repository.daily_details[0][1] == '0000001'
        assert repository.daily_details[0][2] == '001'
        assert repository.daily_details[0][3] == '20200816100000'
        assert repository.daily_details[0][4] == '5000'


