from pprint import pprint
import numpy as np
import hardCoded
import yfinance as yf
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor
from sklearn.neighbors import KNeighborsRegressor
import pandas as pd
from sklearn.neural_network import MLPRegressor
from sklearn.preprocessing import MinMaxScaler
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, r2_score
 
pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)


plt.style.use('dark_background')


class StockAnalyzerController:
    def __init__(self, stock="SPY"):
        self._stock = stock
        self._time_frame = '1y'
        self._active_data = None
        self._chart_data = None
        self._ml_data = None
        self._daily_time_frame = "5m"
        self._stock_info = None
        self._finances = []
        self._chart_value = "Close"
        self._options_data = None
        self._live_snapshot = None
        self._sma = None
        self._ema = None
        self._rsi = None
        self._MACD = None
        self._bollinger = None
        self._envelopes = None
        self._rate_of_change = None
        self._all_techs = None
        self._willaims_R = None
        self._stochastic = None
        self._news_sentiment = None
        self._technical_sentiment = None
        self._news = None
        self._good_to_buy = None
        self._all_sentiment = None

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
        data = yf.Ticker(self._stock)
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

        # Clear Technicals when new stock is selcted
        self._sma = None
        self._ema = None
        self._rsi = None
        self._MACD = None
        self._bollinger = None
        self._envelopes = None
        self._rate_of_change = None
        self._technical_sentiment = None
        self._news_sentiment = None
        self._news = None
        self._all_sentiment = None
        self._good_to_buy = None
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

    def set_ml_data(self, data):
        """
        Sets the ML data
        """
        self._ml_data = data

    def clear_sma(self):
        """
        Reseting sma 
        """
        self._sma = None

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
        if self._stock_info == None:
            self.fetch_stock_information()
        return self._stock_info

    def get_chart(self, root):
        """
        Takes in stock name, time frame, and data 
        and returns a chart

        by default the chart will be built on close prices 

        """

        if self._chart_data is None:
            self.fetch_data_range()

        if self._time_frame == "1d":
            small_range_data = yf.Ticker(self._stock).history(
                interval="1m", period=self._time_frame)
            self._chart_data = small_range_data

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
        if self._options_data == None:
            self.fetch_options_info()

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

    def get_sma(self):
        """
        Returns sma if there is data stored within it 
        """
        if self._sma != {}:
            return self._sma
        else:
            return "Please calculate SMA's before retrival"

    def get_ema(self):
        """
        Returns ema if there is data stored within it 
        """
        if self._ema != {}:
            return self._sma
        else:
            return "Please calculate the EMA's before retrival"

    def get_macd(self):
        """
        Returns the MACD if it has been calculated
        """
        if self._MACD == None:
            return "Please calculate the MACD before retrival"
        else:
            return self._MACD

    def get_RSI(self):
        """
        Runs the rsi method on listed periods 
        stores result in object
        """
        # Get data now, so only need to fetch once
        self.set_time_frame("1y")
        self.fetch_data_range()

        periods = [7, 9, 14, 21, 28, 50, 100, 200]
        rsi_holder = {}

        fourteen_day = None

        # Build objext
        for i in periods:
            rsi = self.calculate_RSI(i)
            # Check the bullish v bearish sentiment
            status = None
            if rsi < 30:
                if i == 14:
                    fourteen_day = "Bullish"
                status = "Bullish, oversold market."
            elif 30 < rsi < 70:
                if i == 14:
                    fourteen_day = "Neutral"
                status = "Neutral"
            else:
                if i == 14:
                    fourteen_day = "Bearish"
                status = "Bearish, overbought market"
            rsi_holder[str(i)] = {
                "rsi": rsi,
                "status": status
            }

        rsi_holder["status"] = fourteen_day

        # Set and return object
        self._rsi = rsi_holder

        return self._rsi

    def get_bollinger(self):
        """
        Returns bollinger bands calculation
        """
        if self._bollinger == None:
            self.calculate_Bollinger_Bands()
        return self._bollinger

    def get_envelopes(self):
        """
        Returns enevlopes calculation
        """
        if self._envelopes == None:
            self.calculate_moving_average_enevelope()
        return self._envelopes

    def get_rate_of_change(self):
        """
        Returns rate of change 
        """
        if self._rate_of_change == None:
            self.calculate_rate_of_change()
        return self._rate_of_change

    def get_all_techincals(self):
        """
        Checks if techs have been caclauted then returns
        """

        if self._all_techs == None:
            self.calculate_all_techincals()

        return self._all_techs

    def get_news_sentiment(self):
        """
        Return sentiment of news
        """
        if self._news is None and self._news_sentiment is None:
            self.process_news_sentiment()

        return self._news_sentiment

    def get_good_to_buy(self):
        """
        Return good to buy calculation 
        """
        if self._good_to_buy == None:
            self.process_good_to_buy()

        return self._good_to_buy

    # Predicitive Models ----------------------------------------------------------------------------
    def neural_network(self, root):
        """
        Using scikit-learn ML library, uses the neural network MLP regressor to 
        make a prediction on the next days closing price, needs to be optomized
        """
        # Pull Data
        data = yf.Ticker(self._stock).history(
            interval="1d", period='5y')
        self.set_ml_data(data)
        data = self._ml_data
        close_prices = data['Close'].values
        training_data = close_prices

        # creating / formatting data
        x_train = np.arange(1, len(training_data) + 1).reshape(-1, 1)
        y_train = training_data.ravel()

        model = MLPRegressor(hidden_layer_sizes=(87,), solver="adam",
                             random_state=1, max_iter=500).fit(x_train, y_train)

        x_test = np.array(len(training_data) + 1).reshape(-1, 1)

        predicted_price = model.predict(x_test)[0]

        fig = Figure(figsize=(8, 5))
        ax = fig.add_subplot(1, 1, 1)

        # Plot the last 30 days of training data
        ax.plot(range(0, 31), y_train[-31:],
                label='Training Data', color='blue')

        # Plot the predicted price for the next day
        ax.scatter(31, predicted_price, color='red', marker='o',
                   label=f'Predicted Price: {predicted_price}')

        ax.set_xlabel('Day')
        ax.set_ylabel('Price')
        ax.set_title(
            'Stock Price Prediction for the Next Day using NeuralNetworkMLPRegressor')
        ax.legend()

        canvas = FigureCanvasTkAgg(fig, master=root)
        canvas_widget = canvas.get_tk_widget()
        canvas_widget.place(x=150, y=200)  # Adjust the coordinates as needed

        canvas.draw()

        return canvas

    def neural_network_accuracy_test(self):
        # Fetch and process data
        data = yf.Ticker(self._stock).history(interval="1d", period='max')
        self.set_ml_data(data)
        data = self._ml_data
        close_prices = data['Close'].values
        print("Cloeses:", len(close_prices))
        # Train-test split
        X_train, X_test, y_train, y_test = train_test_split(
            np.arange(1, len(close_prices) + 1).reshape(-1, 1),
            close_prices.ravel(),
            test_size=0.2,
            random_state=42
        )

        # Train the neural network model
        model = MLPRegressor(hidden_layer_sizes=(
            120,), solver="adam", random_state=1, max_iter=500)
        model.fit(X_train, y_train)

        # Predict on the test set
        y_pred = model.predict(X_test)

        # Calculate and print metrics
        mse = mean_squared_error(y_test, y_pred)
        r2 = r2_score(y_test, y_pred)

        print(f'Mean Squared Error: {mse}')
        print(f'R-squared: {r2}')

    def nearest_nehibor(self, root):
        """
        Utliszed library to implement KNeighbors Regression 
        analysis 

        returns next days predicetd value based on 5y of data
        """
        # Pull Data
        data = yf.Ticker(self._stock).history(
            interval="1d", period='5y')
        self.set_ml_data(data)
        data = self._ml_data
        close_prices = data['Close'].values

        # init features ** All except the last value **
        X = close_prices.reshape(-1, 1)
        y = close_prices.ravel()

        # init nearest neighbor model
        model = KNeighborsRegressor(n_neighbors=100)
        # Train model
        model.fit(X, y)

        # Get previous day close
        previous_day_close = close_prices[-1].reshape(1, -1)

        # predict based on previous day close (returns 1 val)
        predictionn = model.predict(previous_day_close)

        fig = Figure(figsize=(8, 5))
        ax = fig.add_subplot(1, 1, 1)

        # Plot the last 30 days of training data
        ax.plot(range(0, 31), y[-31:], label='Training Data', color='blue')

        # Plot the predicted price for the next day
        ax.scatter(31, predictionn, color='red', marker='o',
                   label=f'Predicted Price: {predictionn[0]}')

        ax.set_xlabel('Day')
        ax.set_ylabel('Price')
        ax.set_title(
            'Stock Price Prediction for the Next Day using KNN Regressor')
        ax.legend()

        canvas = FigureCanvasTkAgg(fig, master=root)
        canvas_widget = canvas.get_tk_widget()
        canvas_widget.place(x=150, y=200)  # Adjust the coordinates as needed

        canvas.draw()

        return canvas

    def knn_accuracy_test(self):
        # Pull Data
        data = yf.Ticker(self._stock).history(interval="1d", period='5y')
        self.set_ml_data(data)
        data = self._ml_data
        close_prices = data['Close'].values

        # Split the data into training and testing sets
        X_train, X_test, y_train, y_test = train_test_split(
            close_prices[:-1].reshape(-1, 1), close_prices[1:], test_size=0.2, random_state=42
        )

        # Initialize and train the KNN model
        model = KNeighborsRegressor(n_neighbors=100)
        model.fit(X_train, y_train)

        # Predict on the test set
        y_pred = model.predict(X_test)

        # Calculate and print metrics
        mse = mean_squared_error(y_test, y_pred)
        r2 = r2_score(y_test, y_pred)

        print(f'Mean Squared Error: {mse}')
        print(f'R-squared: {r2}')

    def random_forest_regression(self, root):
        """
        Feteches data based on current stock
        processes data, cleans data, trains model 
        and returns a pedicted value 

        then returns a drawn canvas for tkinter 
        """

        # Fetching and processing data
        five_day_data = yf.Ticker(self._stock).history(
            interval="1d", period='5y')
        self.set_ml_data(five_day_data)
        data = self._ml_data
        closing_prices = data["Close"].values
        training_data = closing_prices

        # creating / formatting data
        x_train = np.arange(1, len(training_data) + 1).reshape(-1, 1)
        y_train = training_data.ravel()

        # Initializing and training the random forest regressor model
        model = RandomForestRegressor(n_estimators=100, random_state=1)
        model.fit(x_train, y_train)

        # Creating a feature for the next day
        x_test = np.array(len(training_data) + 1).reshape(-1, 1)

        # Predicting price for the next day
        predicted_price = model.predict(x_test)[0]

        fig = Figure(figsize=(8, 5))
        ax = fig.add_subplot(1, 1, 1)
        ax.plot(range(1, 31), y_train[-30:],
                label='Training Data', color='blue')
        ax.scatter(31, predicted_price, color='red', marker='o',
                   label=f'Predicted Price: {predicted_price}')
        ax.set_xlabel('Day')
        ax.set_ylabel('Price')
        ax.set_title(
            'Stock Price Prediction for the Next Day using RandomForestRegressor')
        ax.legend()

        # Creating canvas and returning
        canvas = FigureCanvasTkAgg(fig, master=root)
        canvas_widget = canvas.get_tk_widget()
        canvas_widget.place(x=150, y=200)  # Adjust the coordinates as needed

        canvas.draw()

        return canvas
    
    def random_forest_regressor_test(self):
        """
        Testing MSE and R-Squared of random forest regressor     
        """

        # Pull Data
        data = yf.Ticker(self._stock).history(interval="1d", period='5y')
        self.set_ml_data(data)
        data = self._ml_data
        close_prices = data['Close'].values

        # Split the data into training and testing sets
        X_train, X_test, y_train, y_test = train_test_split(
            close_prices[:-1].reshape(-1, 1), close_prices[1:], test_size=0.2, random_state=42
        )
        # Initializing and training the random forest regressor model
        model = RandomForestRegressor(n_estimators=100, random_state=1)
        model.fit(X_train, y_train)

        # Predict on the test set
        y_pred = model.predict(X_test)

        # Calculate and print metrics
        mse = mean_squared_error(y_test, y_pred)
        r2 = r2_score(y_test, y_pred)

        print(f'Mean Squared Error: {mse}')
        print(f'R-squared: {r2}')

    def linear_regression(self, root):
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

        training_data = close_prices

        # creating / formatting data
        x_train = np.arange(1, len(training_data) + 1).reshape(-1, 1)
        y_train = training_data.ravel()

        # Init linear regression model
        model = LinearRegression().fit(x_train, y_train)

        # Creating a feature for the next day
        x_test = np.array(len(training_data) + 1).reshape(-1, 1)

        # Predicting price for the next day
        predicted_price = model.predict(x_test)[0]

        fig = Figure(figsize=(8, 5))
        ax = fig.add_subplot(1, 1, 1)
        ax.plot(range(1, 31), y_train[-30:],
                label='Training Data', color='blue')
        ax.scatter(31, predicted_price, color='red', marker='o',
                   label=f'Predicted Price: {predicted_price}')
        ax.set_xlabel('Day')
        ax.set_ylabel('Price')
        ax.set_title(
            'Stock Price Prediction for the Next Day using LinearRegression')
        ax.legend()

        # Creating canvas and returning
        canvas = FigureCanvasTkAgg(fig, master=root)
        canvas_widget = canvas.get_tk_widget()
        canvas_widget.place(x=150, y=200)  # Adjust the coordinates as needed

        canvas.draw()

        return canvas

    # Indicators -----------------------------------------------------------------------------------
    def calculate_SMA(self):
        """
        Calculates common SMA's based 
        current stock selected 
        """

        # Updating data reqs
        if self._active_data is None:
            self.set_time_frame("1y")

        else:
            if len(self._active_data) <= 200:
                self.set_time_frame("1y")

        data = self._active_data

        closes = data["Close"].values

        # Calculating SMA's
        three_day = sum(closes[-3:]) / 3
        five_day = sum(closes[-5:]) / 5
        ten_day = sum(closes[-10:]) / 10
        tweleve_day = sum(closes[-12:]) / 12
        twenty_day = sum(closes[-20:]) / 20
        twenty_one_day = sum(closes[-21:]) / 21
        twenty_six_day = sum(closes[-26:]) / 26
        thirty_day = sum(closes[-30:]) / 30
        fifty_day = sum(closes[-50:]) / 50
        hundred_day = sum(closes[-100:]) / 100
        two_hundered_day = sum(closes[-200:]) / 200

        # Storing in Object
        sma = {
            "3": three_day,
            "5": five_day,
            "10": ten_day,
            "12": tweleve_day,
            "20": twenty_day,
            "21": twenty_one_day,
            "26": twenty_six_day,
            "30": thirty_day,
            "50": fifty_day,
            "100": hundred_day,
            "200": two_hundered_day,
        }

        if sma["50"] > sma["200"]:
            sma["status"] = "Bullish"
        else:
            sma["status"] = "Bearish"

        # Updating sma member
        self._sma = sma

    def calculate_EMA(self):
        """
        Calcualtes the ema price for popular periods 
        """

        # Get and prep data
        price_data = self._active_data
        closes = price_data["Close"].values

        # Calcualte sma's if not already calculated
        if self._sma is None:
            self.calculate_SMA()

        # Get all previous smas
        prev_sma = self._sma
        emas = [3, 5, 10, 12, 20, 21, 26, 30, 50, 100, 200]

        # Init objext to hold emas
        ema_holder = {}

        # Complete caluation on all days provided
        for day in emas:
            alpha = 2 / (day + 1)
            ema_price = (1 - alpha) * prev_sma[str(day)] + alpha * closes[-1]
            ema_holder[str(day)] = ema_price

        # Check bearish v bullish with golden cross
        if ema_holder["50"] > ema_holder["200"]:
            ema_holder["status"] = "Bullish"
        else:
            ema_holder["status"] = "Bearish"

        # Update ema memeber
        self._ema = ema_holder

    def calculate_RSI(self, days):
        """
        Calcuates RSI on current stock selected 
        """

        # Get and set data
        price_data = self._active_data
        closes = price_data["Close"].values
        amount_of_prices = closes[-int(days + 1):]

        # Track gains and losses
        net_gain = 0
        net_loss = 0  # Needs to be pos

        for index, close in enumerate(amount_of_prices):
            if index == 0:
                """
                # Skip first index
                # Will get last n + 1 close prices
                # Skip first as the 'first' will be at index 1
                # to find the 'first' gain / loss we need to subtract against this 0th day
                """
                pass
            else:
                # Calcuate whether net gain or loss
                pl = close - amount_of_prices[index - 1]
                if pl > 0:
                    net_gain += pl
                else:
                    net_loss -= pl

        # Get average gain / loss
        average_gain = net_gain / (days)
        average_loss = (net_loss / days)

        # find realtive strength
        relative_stength = average_gain / average_loss

        # Find rsi
        relative_stength_index = 100 - (100/(1+relative_stength))

        # Return result
        return relative_stength_index

    def calculate_MACD(self):
        """
        Calcuates the MACD line of the last closing 
        price
        """
        # Only get emas if they havent already been gotten
        if self._ema is None:
            self.calculate_EMA()

        # Store EMA objext
        emas = self.get_ema()

        # Calcuate MACD Line and set
        macd_line = emas["12"] - emas["26"]
        self._MACD = macd_line

    def calculate_Bollinger_Bands(self):
        """
        Returns bollinger band prices 
        """

        # Check is SMA has been calculated
        if self._sma is None:
            self.calculate_SMA()

        # Set Sma and 20 day window
        smas = self._sma
        middle_band = smas["20"]

        # Get data points
        data = self.get_active_data()["Close"].values
        window = 20

        # Calcuted Standard Deviation
        sqr_dif = [(x - middle_band) ** 2 for x in data[-window:]]
        variance = sum(sqr_dif) / window
        std_dv = variance ** .5

        # Parameter -- Industry standard
        k = 2

        # Calulate upper and lower band
        upper_band = middle_band + k * std_dv
        lower_band = middle_band - k * std_dv

        # Hold objext
        bands = {
            'lower_band': lower_band,
            'middle_band': middle_band,
            'upper_band': upper_band
        }

        # Check sentiment
        if data[-1] < bands["lower_band"]:
            bands["status"] = "Bullish"
        else:
            bands["status"] = "Neutral"
        if data[-1] > bands["upper_band"]:
            bands["status"] = "Bearish"
        else:
            bands["status"] = "Neutral"

        # Set bollinger band data
        self._bollinger = bands

    def calculate_moving_average_enevelope(self):
        """
        Calculates the moving average 
        envelopes of all SMA's
        """

        # Check if SMA has already been calculated
        if self._sma is None:
            self.calculate_SMA()

        # Set data
        data = self._sma

        # Temp holder for enevlopes
        envelopes = {}
        periods = [3, 5, 10, 12, 20, 21, 26, 30, 50, 100, 200]

        # Perform calculations
        for i in periods:
            envelopes[str(i)] = {
                'upper': (data[str(i)]) + (data[str(i)] * 0.03),
                'middle': data[str(i)],
                'lower': (data[str(i)]) - (data[str(i)] * 0.03)
            }

        # Check sentiment
        if self._active_data["Close"].values[-1] > envelopes["20"]["upper"]:
            envelopes["status"] = "Bearish"
        elif self._active_data["Close"].values[-1] < envelopes["20"]["lower"]:
            envelopes["status"] = "Bullish"
        else:
            envelopes["status"] = "Neutral"

        # Set _envelopes data memeber
        self._envelopes = envelopes

    def calculate_rate_of_change(self):
        """
        Calculates the rate of change of n periods 
        """

        # Get closing prices
        closing_prices = self._active_data["Close"].values

        # Most recent closing price
        current_price = closing_prices[-1]

        # Init supported periods
        periods = [3, 5, 10, 12, 20, 21, 26, 30, 50, 100, 200]

        # Temp ROC holder
        rate_of_change_by_period = {}

        # Perform operation
        for i in periods:
            rate_of_change_by_period[str(
                i)] = "% " + str(((current_price - closing_prices[-i]) / closing_prices[-i]) * 100)
            if i == 20:
                if ((current_price - closing_prices[-i]) / closing_prices[-i]) * 100 > 0:
                    rate_of_change_by_period["status"] = "Bullish"
                else:
                    rate_of_change_by_period["status"] = "Bearish"

        # Set data
        self._rate_of_change = rate_of_change_by_period

    def calculate_williams_R(self):
        """
        Calculates the willaims R and determines the sentiment 
        based on the value
        """

        if self._active_data is None:
            self.fetch_data_range()
        elif len(self._active_data) <= 45:
            self.set_time_frame("1y")

        # Long Term Period - 50 Days
        data = self._active_data["Close"].values[-50:]
        current_price = data[-1]
        max_high = max(data[:-1])
        min_low = min(data[:-1])

        # Calculation
        r = ((max_high - current_price)/(max_high - min_low)) * -100

        # Holder
        result = {
            "%R": r
        }

        # Check Sentiment
        if r < -80:
            result["status"] = "Bullish"
        elif r > -20:
            result["status"] = "Bearish"
        else:
            result["status"] = "Neutral"
        pprint(result)

        self._willaims_R = result

    def calulate_stochastic(self):
        if self._active_data is None:
            self.fetch_data_range()
        elif len(self._active_data) <= 45:
            self.set_time_frame("1y")

        # Long Term Period - 50 Days
        data = self._active_data["Close"].values[-50:]
        current_price = data[-1]
        max_high = max(data[:-1])
        min_low = min(data[:-1])

        k = ((current_price - min_low)/(max_high - min_low)) * 100

        # Holder
        result = {
            "%K": k
        }

        # Check Sentiment
        if k < 20:
            result["status"] = "Bullish"
        elif k > 80:
            result["status"] = "Bearish"
        else:
            result["status"] = "Neutral"

        self._stochastic = result

    def calculate_all_techincals(self):
        """
        Getting all technicals, and displaying to tkinter 
        """
        if self._all_techs is None:
            self.calculate_SMA()
            self.calculate_EMA()
            self.get_RSI()
            self.calculate_MACD()
            self.calculate_Bollinger_Bands()
            self.calculate_moving_average_enevelope()
            self.calculate_rate_of_change()
            self.calculate_williams_R()
            self.calulate_stochastic()

        data = {
            "sma": self._sma,
            "ema": self._ema,
            "rsi": self._rsi,
            "macd": self._MACD,
            "bollinger_bands": self._bollinger,
            "envelope": self._envelopes,
            "rate_of_change": self._rate_of_change,
            "willaims_r": self._willaims_R,
            "stochastic_oscillator_k": self._stochastic
        }

        self._all_techs = data

    # Process Data, and properly store --------------------------------------------------------------

    def _process_and_set(self, data):
        """
        Will be used to process data and properly store it
        for active data, chart data, and ML data 
        """
        self._chart_data = data

        self._active_data = data

        self._ml_data = data

    def process_sentiment(self):
        """
        Processes all technical and news sentiment  
        and returns bearish, bullish, neutral
        """

        # Chech if indicators have all been calculated

        if self._all_techs is None:
            self.calculate_all_techincals()

        if self._news_sentiment is None:
            self.process_news_sentiment()

        # Grab all technicals
        techs = self._all_techs
        news = self._news_sentiment

        # Temp Holder
        temp_holder = {}

        # pass on macd, return the rest
        for i in techs:
            if i != "macd":
                temp_holder[i] = techs[i]["status"]

        for idx, value in enumerate(news):
            temp_holder[f"Article {idx + 1}"] = news[value]["status"]

        self._all_sentiment = temp_holder

        return self._all_sentiment

    def process_good_to_buy(self):
        """
        Determine if it is a good time to buy, 
        neutral = 0
        bearish = -1
        bullish = 1
        """

        if self._all_sentiment is None:
            self.process_sentiment()

        all_sentiment = self._all_sentiment

        total = 0

        for i in all_sentiment:
            if all_sentiment[i] == "Bullish":
                print("Bullish")
                total += 1
            elif all_sentiment[i] == "Bearish":
                print("Bearish")
                total -= 1

        self._good_to_buy = total

    def process_news_sentiment(self):
        """
        Fetches the news articles for the given stock and 
        determines the sentiment of the news articles 
        """

        # Calculate the news
        if self._news is None:
            self._news = yf.Ticker(self._stock).news

        # Get the news
        temp_news_object = self._news

        # Initialzie the sentiment analyzer
        analyzer = SentimentIntensityAnalyzer()

        # Make sure there is news present
        if len(temp_news_object) >= 1:

            temp_sent_object = {}
            # Determine the bull/neutral/bear status
            for i in temp_news_object:
                title = i["title"]
                vs = analyzer.polarity_scores(title)
                status = None

                if vs["compound"] > 0.5:
                    status = "Bullish"
                elif vs["compound"] < -0.5:
                    status = "Bearish"
                else:
                    status = "Neutral"
                temp_sent_object[title] = {
                    "values": vs,
                    "status": status
                }

            self._news_sentiment = temp_sent_object
        else:
            self._news_sentiment = None


# Usage example
if __name__ == "__main__":

    controller = StockAnalyzerController()
    controller.random_forest_regressor_test()
