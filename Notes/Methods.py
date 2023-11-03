# import modules
from datetime import datetime
import yfinance as yf
import matplotlib.pyplot as plt

# initialize parameters


start_date = datetime(2023, 10, 23)
end_date = datetime(2023, 10, 27)

# get the data (Historical)
# data = yf.download('SPY', start=start_date, end=end_date)
# print(data)

# Get Live Data on Ticker
# data = yf.Ticker('SPY')
# # live_data = data.history(interval="1m", period='5d')
# print(live_data)

# Get information about Apple Inc. (AAPL) . method is interchanable
# info = yf.Ticker('AAPL').balance_sheet
# print(info)

# Fetch historical data for multiple stocks
# data = yf.download(['AAPL', 'MSFT', 'GOOGL'],start='2021-01-01', end='2022-01-01')
# print(data)


# Visualize ---------------------------------------------------
# display on matlab
# plt.figure(figsize = (20,10))
# plt.title('Opening Prices from {} to {}'.format(start_date,
#                                                end_date))
# plt.plot(data['Open'])
# plt.show()
