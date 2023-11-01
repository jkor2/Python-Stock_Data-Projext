import getDate
import yfinance as yf


class Main:
    def __init__(self, stock="SPY", current_date=getDate.get_current_date(), past_date=getDate.seven_days_ago()):
        self._stock = stock
        self._current_date = current_date
        self._past_date = past_date
        self._active_data = []
        self._chart_data = []
        self._ml_data = []

    def load_data(self):
        """
        Public Method  
        Returns default data
        """
        data = yf.download(self._stock, start=self._past_date,
                           end=self._current_date)
        self._process_and_set(data)

    def get_active_data(self):
        """
        Public Method
        Gets the hashed data
        """
        return self._active_data

    def _process_and_set(self, data):
        """
        Will be used to process data and properly store it
        for active data, chart data, and ML data 
        """
        self._active_data = data
        self._chart_data = data
        self._ml_data = data


main = Main()
main.load_data()
data = main.get_active_data()
