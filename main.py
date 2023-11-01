import hardCoded
import yfinance as yf
import matplotlib.pyplot as plt
plt.style.use('dark_background')


class StockAnalyzerController:
    def __init__(self, stock="SPY"):
        self._stock = stock
        self._time_frame = '5d'
        self._active_data = []
        self._chart_data = []
        self._ml_data = []
        self._daily_time_frame = "5m"
        self._stock_info = {}
        self._finances = []
        self._chart_value = "Close"
        self._options_data = {}

    # FETCH Methods ------------------------------------------------------------------------------
    def fetch_data_range(self):
        """
        Public Method  
        Fetches stock data from a range of dates 
        Returns - date, open, high, low, close, adj clos, volume
        """
        data = yf.download(self._stock, period=self._time_frame)
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
        """
        Public method
        Fetches stock information data
        cleanses response to prevent errors
        sets res to stock info data member
        """
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

    def fetch_financials(self):
        """
        Fetches the finances of the current stock selected
        """

        finance = yf.Ticker(self._stock).financials
        self._finances = finance

    def fetch_options_info(self):
        """
        Fetches options chain calls/puts and updates the _options_data
        data memeber
        """

        options_data_calls = yf.Ticker(self._stock).option_chain().calls
        options_data_puts = yf.Ticker(self._stock).option_chain().calls
        option_data = {'calls': options_data_calls, 'puts': options_data_puts}
        self._options_data = option_data

    # SET Methods ------------------------------------------------------------------------------------

    def set_current_stock(self, stock):
        """
        Sets stock and updates data range data 
        """
        self._stock = str(stock)
        self.fetch_data_range()

    def set_time_frame(self, time_frame):
        """
        Sets time frame and updates the data based on the tf range
        """
        self._time_frame = time_frame

        self.fetch_data_range()

    def set_chart_value(self, value):
        """
        Updates chart value based on the first letter 
        to ensure spelling does not cause any error
        """

        if value[0].upper() == "V":
            self._chart_value = "Volume"
        elif value[0].upper() == "O":
            self._chart_value = "Open"
        elif value[0].upper() == "H":
            self._chart_value = "High"
        elif value[0].upper() == "L":
            self._chart_value = "Low"
        elif value[0].upper() == "C":
            self._chart_value = "Close"

    # GET Methods ------------------------------------------------------------------------------------
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

    def get_chart(self):
        """
        Takes in stock name, time frame, and data 
        and returns a chart

        by default the chart will be built on close prices 

        """

        plt.figure(figsize=(10, 5))
        plt.title('{}: {}'.format(self._stock, self._time_frame))
        plt.plot(self._chart_data[self._chart_value])
        plt.show()

    def get_finances(self):
        """
        Returns the companys financial information
        """

        return self._finances

    def get_options_chain(self):
        """
        Returns options data
        """

        return self._options_data

    # Process Data, and properly store --------------------------------------------------------------
    def _process_and_set(self, data):
        """
        Will be used to process data and properly store it
        for active data, chart data, and ML data 
        """
        self._chart_data = data

        self._active_data = data

        self._ml_data = data


# Usage example
if __name__ == "__main__":
    controller = StockAnalyzerController()
    controller.fetch_data_range()
    # print(controller.get_active_data())
    controller.set_current_stock("TSLA")
    controller.set_time_frame('max')
    # controller.fetch_options_info()
    # controller.get_chart()
    # controller.fetch_financials()
    # print(controller.get_finances())
