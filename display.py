import tkinter as tk
from tkinter import ttk
from tkinter import *

import main

# this is a function to get the user input from the text input box

data = main.StockAnalyzerController()


def getInputBoxValue():
    userInput = Stock.get()
    return userInput


root = Tk()

# This is the section of code which creates the main window
root.geometry('1000x750')
root.configure(background='#F0F8FF')
root.title('Main')


# This is the section of code which creates the a label
Label(root, text='Stock Analysis', bg='#F0F8FF',
      font=('arial', 12, 'normal')).place(x=450, y=25)

Label(root, text='Time Frame', bg='#F0F8FF',
      font=('arial', 10, 'normal')).place(x=50, y=75)

curr_stock = Label(root, text='Current Stock: ' + data.get_current_stock(), bg='#F0F8FF',
                   font=('arial', 10, 'normal'))
curr_stock.place(x=350, y=75)


curr_time_frame = Label(root, text='Current Time Frame: ' + data.get_current_time_frame(), bg='#F0F8FF',
                        font=('arial', 10, 'normal'))
curr_time_frame.place(x=500, y=75)

# This is the section of code which creates a text input box
Stock = Entry(root)
Stock.insert(0, "SPY")  # Set default text to "SPY"
Stock.place(x=450, y=50)


# Create a Text widget for displaying the result
result_text = Text(root, bg='#F0F8FF', font=(
    'arial', 10), wrap='word', height=30, width=90)
result_text.place(x=200, y=200)

# Create a vertical scrollbar for the Text widget
scrollbar = Scrollbar(root, command=result_text.yview)
scrollbar.place(x=840, y=205, height=475)
result_text.config(yscrollcommand=scrollbar.set)


selected_option = StringVar(value="5d")

# Function to handle radio button selection


def radio_button_selected():
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
    userInput = getInputBoxValue()
    data.fetch_data_range()
    active_data = data.get_active_data()

    # Convert the active_data (assumed to be a pandas DataFrame) to a formatted string
    formatted_data = active_data.to_string()

    # Update the content of the Text widget with the formatted data
    result_text.delete(1.0, tk.END)  # Clear previous content
    result_text.insert(tk.END, formatted_data)  # Insert new content

# this is the function called when the button is clicked


def set_current_stock():
    userInput = getInputBoxValue()
    data.set_current_stock(userInput)
    curr_stock.config(text='Current Stock: ' + data.get_current_stock())


# this is the function called when the button is clicked


def set_current_time_frame():
    userInput = getInputBoxValue()
    data.set_time_frame(userInput)
    result_text.config(text='Data for Fetch3: ' + userInput)

# this is the function called when the button is clicked


def btnClickFunction4():
    userInput = getInputBoxValue()
    result_text.config(text='Data for Fetch4: ' + userInput)


# This is the section of code which creates a button
Button(root, text='Fetch Data', bg='#FAEBD7', font=('arial', 12, 'normal'),
       command=fetch_stock_data).place(x=450, y=108)


# This is the section of code which creates a button
Button(root, text='Set Stock', bg='#FAEBD7', font=('arial', 8, 'normal'),
       command=set_current_stock).place(x=600, y=47)


# This is the section of code which creates a button
Button(root, text='Fetch3', bg='#FAEBD7', font=('arial', 12, 'normal'),
       command=set_current_time_frame).place(x=550, y=108)


# This is the section of code which creates a button
Button(root, text='Fetch4', bg='#FAEBD7', font=('arial', 12, 'normal'),
       command=btnClickFunction4).place(x=650, y=108)

root.resizable(False, False)
scrollbar = Scrollbar(root, orient="vertical")

root.mainloop()
