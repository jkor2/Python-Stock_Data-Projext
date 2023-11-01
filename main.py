import getDate
import yfinance as yf

# Internal Imports
import hardCoded


class Main:
    def __init__(self, stock="SPY", current_date=getDate.get_current_date(), past_date=getDate.seven_days_ago()):
        self._stock = stock
        self._current_date = current_date
        self._past_date = past_date
        self._active_data = []
        self._chart_data = []
        self._ml_data = []
        self._daily_time_frame = "5m"
        self._stock_info = {}

    def fetch_data_range(self):
        """
        Public Method  
        Fetches stock data from a range of dates 
        Returns - date, open, high, low, close, adj clos, volume
        """
        data = yf.download(self._stock, start=self._past_date,
                           end=self._current_date)
        self._process_and_set(data)

    def fetch_current_day_data(self):
        """
        Public method
        Fetches stock data of current selected stock
        5m timeframe by default
        """
        data = yf.download(
            self._stock, interval=self._daily_time_frame, period='1d')
        self._process_and_set(data)

    def fetch_stock_information(self):
        info = yf.Ticker(self._stock).basic_info
        # Process Info
        info_object = {}

        # Cleanse data - not all stocks have values for keys
        for i in hardCoded.stock_info_keys:
            # Validate there is data present in Key
            try:
                if info[i]:
                    info_object[i] = info[i]
                else:
                    pass
            except:
                pass

        self._stock_info = info_object

    def get_active_data(self):
        """
        Public Method
        Gets the hashed data
        """
        return self._active_data

    def get_stock_info(self):
        """
        Return private stock info data memeber
        """
        return self._stock_info

    def _process_and_set(self, data):
        """
        Will be used to process data and properly store it
        for active data, chart data, and ML data 
        """
        self._active_data = data
        self._chart_data = data
        self._ml_data = data


main = Main()
main.fetch_data_range()
# data = main.get_active_data()
# print(data)
# main.fetch_current_day_data()
# data = main.get_active_data()
# print(data)
main.fetch_stock_information()
print(main.get_stock_info())
