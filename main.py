import getDate
import yfinance as yf


class Main:
    def __init__(self, stock="SPY", current_date=getDate.get_current_date(), past_date=getDate.seven_days_ago()):
        self._stock = stock
        self._current_date = current_date
        self._past_date = past_date

    def default_data(self):
        data = yf.download(self._stock, start=self._past_date,
                           end=self._current_date)
        print(data)


test1 = Main()
