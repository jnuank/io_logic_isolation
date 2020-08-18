from datetime import datetime, date

from source.domain.models.salses.daily_sales import DailySales
from source.domain.models.salses.daily_sales_detail import DailySalesDetail
from source.domain.models.salses.shop_monthly_sales import ShopMonthlySales


class TestShopSalesModel:

    def test_同じ日の複数取引の合計金額を出せる(self):
        detail = DailySalesDetail('0000001', datetime.now(), '001', 10000)
        detail2 = DailySalesDetail('0000001', datetime.now(), '001', 5000)
        result = DailySales(date.today(), [detail, detail2])

        assert result.amount() == 15000

    def test_同じ月の別日売上の合計金額を出せる(self):
        detail = DailySalesDetail('0000001', datetime(2020, 8, 20, 10, 0, 0), '001', 10000)
        detail2 = DailySalesDetail('0000001', datetime(2020, 8, 20, 13, 0, 0), '001', 5000)

        sales_0820 = DailySales(date(2020, 8, 20), [detail, detail2])

        detail3 = DailySalesDetail('0000001', datetime(2020, 8, 21, 14, 0, 0), '001', 2000)
        detail4 = DailySalesDetail('0000001', datetime(2020, 8, 21, 20, 0, 0), '001', 5000)

        sales_0821 = DailySales(date(2020, 8, 21), [detail3, detail4])

        result = ShopMonthlySales('001', '202008', [sales_0820, sales_0821])

        assert result.amount() == 22000