import tkinter as tk
from tkinter import ttk
from tkinter import *
from tabulate import tabulate
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
root.configure(background='#FFFFFF')
root.title('Main')


# Creates the Lables
Label(root, text='Stock Analysis', bg='#FFFFFF',
      font=('arial', 12, 'normal')).place(x=450, y=25)

Label(root, text='Time Frame', bg='#F0F8FF',
      font=('arial', 10, 'normal')).place(x=50, y=75)

curr_stock = Label(root, text='Current Stock: ' + data.get_current_stock(), bg='#F0F8FF',
                   font=('arial', 10, 'normal'))
curr_stock.place(x=350, y=75)


curr_time_frame = Label(root, text='Current Time Frame: ' + data.get_current_time_frame(), bg='#F0F8FF',
                        font=('arial', 10, 'normal'))
curr_time_frame.place(x=500, y=75)

# Creates a text input box
Stock = Entry(root)
Stock.insert(0, "SPY")  # Set default text to "SPY"
Stock.place(x=450, y=50)


# Create a Text widget for displaying the result
result_text = Text(root, bg='#F0F8FF', font=(
    'arial', 10), wrap='word', height=30, width=110)
result_text.place(x=150, y=200)

# Create a vertical scrollbar for the Text widget
scrollbar = Scrollbar(root, command=result_text.yview)
scrollbar.place(x=900, y=205, height=475)
result_text.config(yscrollcommand=scrollbar.set)


# Making 5d the dafault time frame
selected_option = StringVar(value="5d")

# Function to handle radio button selection


def radio_button_selected():
    """
    Handles selection and updates the time frame lable
    """
    data.set_time_frame(selected_option.get())

    curr_time_frame.config(text='Current Time Frame: ' +
                           data.get_current_time_frame())


# Create radio buttons
radio_button1 = Radiobutton(root, text="1 Day", variable=selected_option,
                            value="1d", command=radio_button_selected)
radio_button2 = Radiobutton(root, text="5 Day", variable=selected_option,
                            value="5d", command=radio_button_selected)
radio_button3 = Radiobutton(root, text="1 Month", variable=selected_option,
                            value="1mo", command=radio_button_selected)
radio_button4 = Radiobutton(root, text="3 month", variable=selected_option,
                            value="3mo", command=radio_button_selected)
radio_button5 = Radiobutton(root, text="6 Month", variable=selected_option,
                            value="6mo", command=radio_button_selected)
radio_button6 = Radiobutton(root, text="1 Year", variable=selected_option,
                            value="1y", command=radio_button_selected)
radio_button7 = Radiobutton(root, text="5 Year", variable=selected_option,
                            value="5y", command=radio_button_selected)
radio_button8 = Radiobutton(root, text="YTD", variable=selected_option,
                            value="ytd", command=radio_button_selected)
radio_button9 = Radiobutton(root, text="Max", variable=selected_option,
                            value="MAX", command=radio_button_selected)


# Place the radio buttons on the window
radio_button1.place(x=50, y=100)
radio_button2.place(x=50, y=130)
radio_button3.place(x=50, y=160)
radio_button4.place(x=50, y=190)
radio_button5.place(x=50, y=220)
radio_button6.place(x=50, y=250)
radio_button7.place(x=50, y=280)
radio_button8.place(x=50, y=310)
radio_button9.place(x=50, y=340)


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


def fetch_technicals():
    """
    Returns all Technicals
    """

    techs = data.get_all_techincals()

    global chart_canvas  # Declare chart_canvas as a global variable

    if chart_canvas:  # Delete any canvas if present
        chart_canvas.get_tk_widget().destroy()

    result_text.delete(1.0, tk.END)
    result_text.insert(tk.END, 'Technicals\n')

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


# Xreates a button
Button(root, text='Fetch Technicals', bg='#FAEBD7', font=('arial', 12, 'normal'),
       command=fetch_technicals).place(x=700, y=50)

Button(root, text='Live Snapshot', bg='#FAEBD7', font=('arial', 12, 'normal'),
       command=fetch_snapshot).place(x=700, y=90)


Button(root, text='Fetch Data', bg='#FAEBD7', font=('arial', 12, 'normal'),
       command=fetch_stock_data).place(x=700, y=10)

Button(root, text='Linear Regression', bg='#FAEBD7', font=('arial', 12, 'normal'),
       command=run_regression_mode).place(x=200, y=10)
Button(root, text='Random Forest', bg='#FAEBD7', font=('arial', 12, 'normal'),
       command=run_random_forest).place(x=205, y=50)

Button(root, text='Nearest Neighbors', bg='#FAEBD7', font=('arial', 12, 'normal'),
       command=run_nearest_neighbor).place(x=200, y=90)

Button(root, text='Set Stock', bg='#FAEBD7', font=('arial', 8, 'normal'),
       command=set_current_stock).place(x=600, y=47)

Button(root, text='Fetch Info', bg='#FAEBD7', font=('arial', 12, 'normal'),
       command=get_stock_info).place(x=820, y=10)

Button(root, text='Get Chart', bg='#FAEBD7', font=('arial', 12, 'normal'),
       command=get_chart).place(x=400, y=108)
Button(root, text='Remove Chart', bg='#FAEBD7', font=('arial', 12, 'normal'),
       command=remove_chart).place(x=500, y=108)

root.resizable(False, False)  # Makes not resiazble
scrollbar = Scrollbar(root, orient="vertical")  # Init vertical scroll bar

root.mainloop()
