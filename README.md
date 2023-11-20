# Stock Analyzer Application

**Still a work in progress, updates will be made as done.** 

Video Demo: [Demo](https://www.youtube.com/watch?v=94ulqcBaaxY)

## Description

I'm excited to share this project I've been working on—a predictive stock analysis app with a Tkinter GUI. This project is a testament to the power of Python and various libraries, including Tkinter, Scikit-Learn, Matplotlib, Pandas, NumPy, and others.

The app seamlessly integrates the yfinance API to fetch both historical and live stock and options data. It utilizes this data to perform a range of analyses, including running predictive models, calculating indicators, displaying charts, and conducting sentiment analysis on news headlines related to the selected security.

For predictive modeling, the app takes five years of daily closing levels and employs multiple machine learning models from Scikit-Learn, such as Linear Regressor, KNN Regressor, Random Forest Regressor, or MLPRegressor, depending on the user's preference.

Sentiment analysis is a key feature, incorporating the calculation of technical indicators and leveraging industry-standard interpretations to gauge bullish, bearish, or neutral momentum. The app also employs VectorSentiment for headline sentiment analysis, using eight recent news headlines to determine the overall sentiment—whether it's bullish, bearish, or neutral.

## Key Features

- **Predictive Models:**
  - Implement predictive models like K-Nearest Neighbors, Random Forest Regression, Linear Regression, and MLP Regressor to predict stock prices.

- **Data Fetching:**

  - Fetch historical stock data for a specified time frame.
  - Fetch intraday stock data for the current day.

- **Data Visualization:**

  - View historical stock data using interactive charts.
  - Choose different chart values such as Open, High, Low, Close, and Volume.

- **Financial Information:**

  - Retrieve basic financial information about the selected stock, including market cap, sector, and more.

- **Options Chain:**

  - Fetch and display options chain data, including call and put options.

- **Technical Indicators:**

  - Calculate a variety of technical indicators 
  - Calculate the "Best" time to purschase a stock based on the indicators sentiment
    
- **Sentiment Analysis:**

  - Calculate a sentiment based on technical indicators 
  - Calculate sentiment based on news headlines using VectorSentiment
  

**Not financial advice**
