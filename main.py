import hardCoded
import yfinance as yf
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
import numpy as np

from pprint import pprint
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
        self._live_snapshot = None

    # FETCH Methods ------------------------------------------------------------------------------
    def fetch_data_range(self):
        """
        Public Method  
        Fetches stock data from a range of dates 
        Returns - date, open, high, low, close, adj clos, volume
        """
        data = yf.download(self._stock, period=self._time_frame)
        self._process_and_set(data)

    def fetch_data_day(self):
        """
        Public method
        Fetches stock data of current selected stock
        5m timeframe by default
        """
        data = yf.download(
            self._stock, interval=self._daily_time_frame, period='1d')
        self._process_and_set(data)

    def fetch_live_data(self):
        """
        Fetches the current quote of stock
        sets the snapshot to the value  
        """
        data = yf.Ticker('SPY')
        live_data = data.history(period='1d')
        self._live_snapshot = live_data

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

        finance = yf.Ticker(self._stock).balancesheet
        print(finance)
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

    def get_chart(self, root):
        """
        Takes in stock name, time frame, and data 
        and returns a chart

        by default the chart will be built on close prices 

        """

        fig = Figure(figsize=(8, 5))
        ax = fig.add_subplot(1, 1, 1)
        ax.set_title('{}: {}'.format(self._stock, self._time_frame))
        ax.plot(self._chart_data[self._chart_value])

        canvas = FigureCanvasTkAgg(fig, master=root)  # A tk.DrawingArea.
        canvas_widget = canvas.get_tk_widget()
        canvas_widget.place(x=150, y=200)  # Adjust the coordinates as needed

        canvas.draw()

        return canvas

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

    def get_snapshot(self):
        """
        Updates the snapshot by calling the fetch method
        returns the newly updated data
        """
        self.fetch_live_data()
        return self._live_snapshot

    def get_current_stock(self):
        """
        Returns the current stock
        """
        return self._stock

    def get_current_time_frame(self):
        """
        Returns current time frame 
        """
        return self._time_frame

    # Predicitive Models ----------------------------------------------------------------------------

    def linear_regression(self):
        """
        Takes in a stock, adjust time frame to 1y
        trains based on past 220 days 
        predicst the next 30 days 
        """
        # Adjust time frame
        self.set_time_frame("1y")
        # Fetch Data
        self.fetch_data_range()
        data = self._ml_data
        close_prices = data['Close'].values

        # Training data
        # Use 220 days for training
        train_data = close_prices[:(len(close_prices) - 30)]

        # Testing data (last 30 days)
        test_data = close_prices[-30:]

        # Even spaced array, 2d array reshape
        x_train = np.arange(1, len(train_data) + 1).reshape(-1, 1)
        y_train = train_data.reshape(-1, 1)

        # Init linear regression model
        model = LinearRegression()
        # Train model
        model.fit(x_train, y_train)

        # Create evennly spaced array and reshape into 2d single collumn array
        x_test = np.arange(len(train_data) + 1, len(train_data) +
                           len(test_data) + 1).reshape(-1, 1)

    # Flatten the predicted_prices array - convert to 1D array
        predicted_prices = model.predict(x_test).flatten()

    # Use the entire dataset for all_days
        all_days = np.arange(1, len(close_prices) + 1)

    # Concatenate the actual closing prices and predicted closing prices
        all_prices = np.concatenate([close_prices[:-30], predicted_prices])

    # Visualize all 250 days of closing prices
        plt.figure(figsize=(10, 6))
        plt.plot(all_days[:len(close_prices) - 30], all_prices[:len(close_prices) - 30],
                 label='Actual Closing Prices', color='blue')
        plt.plot(all_days[len(close_prices) - 30:], all_prices[len(close_prices) -
                                                               30:], label='Predicted Closing Prices', color='red')
        plt.axvline(x=len(close_prices) - 30, color='gray', linestyle='--',
                    linewidth=1)  # Separating actual and predicted prices
        plt.xlabel('Day')
        plt.ylabel('Closing Price')
        plt.title('Actual vs. Predicted Closing Prices')
        plt.legend()
        plt.grid(True)
        plt.show()

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
    # controller.fetch_data_range()
    # print(controller.get_active_data())
    controller.set_time_frame('max')
    controller.set_current_stock("AAPL")
    # controller.set_time_frame('ytd')
    # controller.fetch_stock_information()
    # pprint(controller.get_stock_info())
    # controller.fetch_options_info()
    # controller.get_options_chain()
    # controller.get_chart()

    controller.fetch_data_range()
    controller.linear_regression()
    # print(controller.fetch_live_data())
