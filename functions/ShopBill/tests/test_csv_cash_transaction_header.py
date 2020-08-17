from source.domain.models.csv_models.csv_cash_transaction_header import CsvCashTransactionHeader


class TestCsvCashTransactionHeader:

    def test_ヘッダモデルが作成されること(self):

        results = CsvCashTransactionHeader.from_csv('cash_register.csv')

        assert results[0].shop_code == '1'
        assert results[0].cash_register_code == '1'
        assert results[0].transaction_code == '0000001'
        assert results[0].transaction_datetime == '20200816100000'

        assert results[0].transaction_details[0].item_name == '商品A'
        assert results[0].transaction_details[0].unit_price == 1000
        assert results[0].transaction_details[0].quantity == 2
