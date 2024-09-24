import random
import unittest

from data_download import fetch_stock_data, calculate_and_display_average_price, notify_if_strong_fluctuations


stocks = ["AAPL", "FF", "DAX", "GOOG", "AMZN"]
period = ["1d", "1mo", "1y"]


class RunTest(unittest.TestCase):
    def setUp(self):
        self.stock_data = fetch_stock_data(random.choice(stocks), random.choice(period))

    def test_type_answer_for_average_price(self):
        msg = "Другой тип данных"
        average_price = calculate_and_display_average_price(self.stock_data)
        self.assertIsInstance(average_price, float, msg)

    def test_get_notification(self):
        msg = "Уведомление не пришло"
        average_price = notify_if_strong_fluctuations(self.stock_data, 0.001)
        self.assertIsInstance(average_price, str, msg)


if __name__ == '__main__':
    unittest.main()