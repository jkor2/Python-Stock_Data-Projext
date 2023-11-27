import tkinter as tk
from tkinter import *
import pprint


import main

# this is a function to get the user input from the text input box

data = main.StockAnalyzerController()


def getInputBoxValue():
    """
    Gets the users input from the text field
    """
    userInput = Stock.get()
    return userInput


# Init root
root = Tk()

# cXeates the main window
root.geometry('1000x750')
root.configure(background='#1E1E1E')
root.title('Main')


# Creates the Lables
Label(root, text='Stock Analysis', bg='#1E1E1E', fg='#FFFFFF',
      font=('arial', 20, 'bold')).place(x=415, y=5)

Label(root, text='Time Frame', bg='#1E1E1E',fg='#FFFFFF',
      font=('arial', 10, 'bold')).place(x=45, y=290)

Label(root, text='Predictive Models', bg='#1E1E1E',fg='#FFFFFF',
      font=('arial', 12, 'bold')).place(x=10, y=10)

Label(root, text='Sentiment', bg='#1E1E1E',fg='#FFFFFF',
      font=('arial', 12, 'bold')).place(x=200, y=10)

Label(root, text='Stock Data', bg='#1E1E1E',fg='#FFFFFF',
      font=('arial', 12, 'bold')).place(x=725, y=10)

Label(root, text='Stock Info', bg='#1E1E1E',fg='#FFFFFF',
      font=('arial', 12, 'bold')).place(x=875, y=10)


curr_stock = Label(root, text='Current Stock: ' + data.get_current_stock(), bg='#1E1E1E',fg='#FFFFFF',
                   font=('arial', 10, 'bold'))
curr_stock.place(x=450, y=80)


curr_time_frame = Label(root, text='Current Time Frame: ' + data.get_current_time_frame(), bg='#1E1E1E',fg='#FFFFFF',
                        font=('arial', 10, 'bold'))
curr_time_frame.place(x=450, y=100)

# Creates a text input box
Stock = Entry(root)
Stock.insert(0, "SPY")  # Set default text to "SPY"
Stock.place(x=450, y=50)


# Create a Text widget for displaying the result
result_text = Text(root, bg='#1E1E1E', fg='#FFFFFF', font=('arial', 10),
                   wrap='word', height=30, width=110)
result_text.place(x=150, y=200)

# Create a vertical scrollbar for the Text widget
scrollbar = Scrollbar(root, command=result_text.yview)
scrollbar.place(x=900, y=205, height=475)
result_text.config(yscrollcommand=scrollbar.set)


# Making 5d the dafault time frame
selected_option = StringVar(value="1y")

# Function to handle radio button selection


def radio_button_selected():
    """
    Handles selection and updates the time frame lable
    """
    data.set_time_frame(selected_option.get())

    curr_time_frame.config(text='Current Time Frame: ' +
                           data.get_current_time_frame())


# Create radio buttons
radio_button1 = Radiobutton(root, bg="#1E1E1E",selectcolor="#3498db" , fg='#FFFFFF',text="1 Day", variable=selected_option,
                            value="1d", command=radio_button_selected)
radio_button2 = Radiobutton(root, bg="#1E1E1E",  selectcolor="#3498db" ,fg='#FFFFFF',text="5 Day", variable=selected_option,
                            value="5d", command=radio_button_selected)
radio_button3 = Radiobutton(root, bg="#1E1E1E",selectcolor="#3498db" ,  fg='#FFFFFF',text="1 Month", variable=selected_option,
                            value="1mo", command=radio_button_selected)
radio_button4 = Radiobutton(root, bg="#1E1E1E", selectcolor="#3498db" , fg='#FFFFFF',text="3 month", variable=selected_option,
                            value="3mo", command=radio_button_selected)
radio_button5 = Radiobutton(root, bg="#1E1E1E", selectcolor="#3498db" , fg='#FFFFFF',text="6 Month", variable=selected_option,
                            value="6mo", command=radio_button_selected)
radio_button6 = Radiobutton(root, bg="#1E1E1E",selectcolor="#3498db" , fg='#FFFFFF', text="1 Year", variable=selected_option,
                            value="1y", command=radio_button_selected)
radio_button7 = Radiobutton(root, bg="#1E1E1E", selectcolor="#3498db" , fg='#FFFFFF',text="5 Year", variable=selected_option,
                            value="5y", command=radio_button_selected)
radio_button8 = Radiobutton(root, bg="#1E1E1E", selectcolor="#3498db" , fg='#FFFFFF',text="YTD", variable=selected_option,
                            value="ytd", command=radio_button_selected)
radio_button9 = Radiobutton(root, bg="#1E1E1E", selectcolor="#3498db" , fg='#FFFFFF',text="Max", variable=selected_option,
                            value="MAX", command=radio_button_selected)


# Place the radio buttons on the window
radio_button1.place(x=50, y=310)
radio_button2.place(x=50, y=340)
radio_button3.place(x=50, y=370)
radio_button4.place(x=50, y=400)
radio_button5.place(x=50, y=430)
radio_button6.place(x=50, y=460)
radio_button7.place(x=50, y=490)
radio_button8.place(x=50, y=520)
radio_button9.place(x=50, y=550)


def fetch_stock_data():
    """
    Loads the stock data
    """

    global chart_canvas  # Declare chart_canvas as a global variable

    if chart_canvas:  # Delete any canvas if present
        chart_canvas.get_tk_widget().destroy()

    data.fetch_data_range()
    active_data = data.get_active_data()

    formatted_data = active_data.to_string()

    result_text.delete(1.0, tk.END)  # Clear previous content
    result_text.insert(tk.END, formatted_data)  # Insert new content


def set_current_stock():
    """
    Sets the current stock and updates lable
    """
    userInput = getInputBoxValue()
    data.set_current_stock(userInput)
    curr_stock.config(text='Current Stock: ' + data.get_current_stock())


# this is the function called when the button is clicked


def get_stock_info():
    """
    Gets stock info from main class handling API
    """

    global chart_canvas  # Declare chart_canvas as a global variable

    if chart_canvas:  # Delete any canvas if present
        chart_canvas.get_tk_widget().destroy()

    data.fetch_stock_information()
    data.fetch_financials()
    stock_info = data.get_stock_info()
    stock_finances = data.get_finances()
    result_text.delete(1.0, tk.END)
    result_text.insert(tk.END, 'Basic Information\n')
    for key, value in stock_info.items():
        # Insert new content with a newline character after each item
        result_text.insert(tk.END, f'{key}: {value}\n')
    result_text.insert(tk.END, 'Balance Sheet\n')
    result_text.insert(tk.END, stock_finances)


chart_canvas = None  # Init canvas so it is only None Once


def get_chart():
    """
    Gets stock chart from main class handling API
    """
    global chart_canvas  # Declare chart_canvas as a global variable

    # Check if chart_canvas exists and destroy it if it does
    if chart_canvas:
        chart_canvas.get_tk_widget().destroy()

    chart_canvas = data.get_chart(root)
    chart_canvas.get_tk_widget().pack(fill=tk.NO, expand=False)

    # result_text.config(text='Data for Fetch4: ' + userInput)


def remove_chart():
    """
    Removes chart canvas from the GUI
    """
    if chart_canvas:
        chart_canvas.get_tk_widget().destroy()


def run_regression_mode():
    """
    Runs the regression model
    returns a fugure dispalying
    predictions for next 50 days
    """

    global chart_canvas  # Declare chart_canvas as a global variable

    if chart_canvas:  # Delete any canvas if present
        chart_canvas.get_tk_widget().destroy()

    # Update radio and time frame
    data.set_time_frame("1y")
    selected_option.set("1y")
    curr_time_frame.config(text='Current Time Frame: ' +
                           data.get_current_time_frame())

    # Display figure from controller
    chart_canvas = data.linear_regression(root)
    chart_canvas.get_tk_widget().pack(fill=tk.NO, expand=False)


def run_random_forest():
    """
    Calls the random forest regression method from 
    the controller, returns and posts a canvas visual 
    """
    global chart_canvas  # Declare chart_canvas as a global variable

    if chart_canvas:  # Delete any canvas if present
        chart_canvas.get_tk_widget().destroy()

    data.set_time_frame("5y")
    selected_option.set("5y")
    curr_time_frame.config(text='Current Time Frame: ' +
                           data.get_current_time_frame())

    # Display figure from controller
    chart_canvas = data.random_forest_regression(root)
    chart_canvas.get_tk_widget().pack(fill=tk.NO, expand=False)


def run_nearest_neighbor():
    """
    calls nearest neightbor method from 
    controller class

    returns canvas to display on tkinter
    """
    global chart_canvas  # Declare chart_canvas as a global variable

    if chart_canvas:  # Delete any canvas if present
        chart_canvas.get_tk_widget().destroy()

    data.set_time_frame("5y")
    selected_option.set("5y")
    curr_time_frame.config(text='Current Time Frame: ' +
                           data.get_current_time_frame())

    chart_canvas = data.nearest_nehibor(root)
    chart_canvas.get_tk_widget().pack(fill=tk.NO, expand=False)


def run_neural_network():
    """
    Returns the chart of the MLP Regressor predicted price 
    """
    global chart_canvas  # Declare chart_canvas as a global variable

    if chart_canvas:  # Delete any canvas if present
        chart_canvas.get_tk_widget().destroy()

    data.set_time_frame("5y")
    selected_option.set("5y")
    curr_time_frame.config(text='Current Time Frame: ' +
                           data.get_current_time_frame())

    chart_canvas = data.neural_network(root)
    chart_canvas.get_tk_widget().pack(fill=tk.NO, expand=False)


def fetch_technicals():
    """
    Returns all Technicals
    """

    global chart_canvas  # Declare chart_canvas as a global variable

    if chart_canvas:  # Delete any canvas if present
        chart_canvas.get_tk_widget().destroy()

    techs = data.get_all_techincals()

    result_text.delete(1.0, tk.END)
    result_text.insert(tk.END, 'Sentiment\n')

    result_text.insert(tk.END, pprint.pformat(techs))  # Format with pprint


def fetch_sentiment_indicators():
    """
    Get all indicators sentiment
    """
    global chart_canvas  # Declare chart_canvas as a global variable

    if chart_canvas:  # Delete any canvas if present
        chart_canvas.get_tk_widget().destroy()

    techs = data.process_sentiment()

    result_text.delete(1.0, tk.END)
    result_text.insert(tk.END, 'Sentiment\n')

    gtb = data.get_good_to_buy()

    status = ""

    if gtb == 0:
        status = "Based on sentiment, there is uncertantity within the market"
    elif gtb > 0:
        status = "Based on sentiment, technicals and headlines point to bullish momentum"
    else:
        status = "Based on sentiment, technicals and headlines point to bearish momentum"

    result_text.insert(tk.END, pprint.pformat(techs))  # Format with pprint
    result_text.insert(tk.END, "\n")
    result_text.insert(tk.END, status)


def fetch_news_sentiment():
    """
    Displays news sentiment calcultions  
    """

    global chart_canvas  # Declare chart_canvas as a global variable

    if chart_canvas:  # Delete any canvas if present
        chart_canvas.get_tk_widget().destroy()

    techs = data.get_news_sentiment()

    result_text.delete(1.0, tk.END)
    result_text.insert(tk.END, 'News Sentiment\n')

    result_text.insert(tk.END, pprint.pformat(techs))  # Format with pprint


def fetch_snapshot():
    """
    Displays a live snapshot
    """
    global chart_canvas  # Declare chart_canvas as a global variable

    if chart_canvas:  # Delete any canvas if present
        chart_canvas.get_tk_widget().destroy()

    snap_shot = data.get_snapshot()

    result_text.delete(1.0, tk.END)
    result_text.insert(tk.END, 'Live Snapshot \n')

    result_text.insert(tk.END, pprint.pformat(snap_shot))  # Format with pprint


def fetch_calls():
    """
    Displays options chain data - calls
    """
    if chart_canvas:  # Delete any canvas if present
        chart_canvas.get_tk_widget().destroy()

    options_data = data.get_options_chain()

    result_text.delete(1.0, tk.END)
    result_text.insert(tk.END, 'Live Snapshot \n')

    result_text.insert(tk.END, pprint.pformat(
        options_data["calls"]))  # Format with pprint


def fetch_puts():
    """
    Displays options chain data - puts
    """

    if chart_canvas:  # Delete any canvas if present
        chart_canvas.get_tk_widget().destroy()

    options_data = data.get_options_chain()

    result_text.delete(1.0, tk.END)
    result_text.insert(tk.END, 'Live Snapshot \n')

    result_text.insert(tk.END, pprint.pformat(
        options_data["puts"]))  # Format with pprint


# Xreates a button
Button(root, text='Technical Sentiment', width='15',bg='#353535', font=('arial', 12, 'normal'), fg='#FFFFFF',
       command=fetch_technicals).place(x=200, y=40)

Button(root, text='All Sentiment', width='15',bg='#353535', font=('arial', 12, 'normal'), fg='#FFFFFF',
       command=fetch_sentiment_indicators).place(x=200, y=120)

Button(root, text='News Sentiment', width='15',bg='#353535', font=('arial', 12, 'normal'), fg='#FFFFFF',
       command=fetch_news_sentiment).place(x=200, y=80)


Button(root, text='Live Snapshot', width='15',bg='#353535', font=('arial', 12, 'normal'), fg='#FFFFFF',
       command=fetch_snapshot).place(x=700, y=80)

Button(root, text='Get Calls', width='15',bg='#353535', font=('arial', 12, 'normal'), fg='#FFFFFF',
       command=fetch_calls).place(x=700, y=120)

Button(root, text='Get Puts', width='15',bg='#353535', font=('arial', 12, 'normal'), fg='#FFFFFF',
       command=fetch_puts).place(x=700, y=160)


Button(root, text='Fetch Data', width='15', bg='#353535', font=('arial', 12, 'normal'), fg='#FFFFFF',
       command=fetch_stock_data).place(x=700, y=40)

Button(root, text='Linear Regression', width='15', bg='#353535', font=('arial', 12, 'normal'), fg='#FFFFFF',
       command=run_regression_mode).place(x=10, y=40)
Button(root, text='Random Forest', width='15', bg='#353535', font=('arial', 12, 'normal'), fg='#FFFFFF',
       command=run_random_forest).place(x=10, y=80)

Button(root, text='Nearest Neighbors', width='15', bg='#353535', font=('arial', 12, 'normal'), fg='#FFFFFF',
       command=run_nearest_neighbor).place(x=10, y=120)

Button(root, text='Neural Network', width='15',bg='#353535', font=('arial', 12, 'normal'), fg='#FFFFFF',
       command=run_neural_network).place(x=10, y=160)

Button(root, text='Set Stock', bg='#353535', font=('arial', 8, 'normal'), fg='#FFFFFF',
       command=set_current_stock).place(x=600, y=47)

Button(root, text='Fetch Info', width='15',bg='#353535', font=('arial', 12, 'normal'), fg='#FFFFFF',
       command=get_stock_info).place(x=850, y=40)

Button(root, text='Get Chart', bg='#353535', font=('arial', 12, 'normal'), fg='#FFFFFF',
       command=get_chart).place(x=420, y=135)
Button(root, text='Remove Chart',bg='#353535', font=('arial', 12, 'normal'), fg='#FFFFFF',
       command=remove_chart).place(x=510, y=135)

root.resizable(False, False)  # Makes not resiazble
scrollbar = Scrollbar(root, orient="vertical", bg="#1E1E1E")  # Init vertical scroll bar

root.mainloop()
