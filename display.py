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

curr_stock = Label(root, text='Current Stock: ' + data.get_current_stock(), bg='#F0F8FF',
                   font=('arial', 10, 'normal'))
curr_stock.place(x=450, y=75)


# This is the section of code which creates a text input box
Stock = Entry(root)
Stock.insert(0, "SPY")  # Set default text to "SPY"
Stock.place(x=450, y=50)


result_label = Label(root, text='', bg='#F0F8FF', font=(
    'arial', 12, 'normal'), anchor='center')
result_label.place(x=200, y=325)  # Adjust the position as needed


def btnClickFunction1():
    userInput = getInputBoxValue()  # Gets the value from the input
    data.fetch_data_range()
    active_data = data.get_active_data()
    current_stock = data.get_current_stock()
    result_label.config(text='Data for ' + current_stock + str(active_data))

# this is the function called when the button is clicked


def btnClickFunction2():
    userInput = getInputBoxValue()
    data.set_current_stock(userInput)
    curr_stock.config(text='Current Stock: ' + data.get_current_stock())


# this is the function called when the button is clicked


def btnClickFunction3():
    userInput = getInputBoxValue()
    result_label.config(text='Data for Fetch3: ' + userInput)

# this is the function called when the button is clicked


def btnClickFunction4():
    userInput = getInputBoxValue()
    result_label.config(text='Data for Fetch4: ' + userInput)


# This is the section of code which creates a button
Button(root, text='Fetch Data', bg='#FAEBD7', font=('arial', 12, 'normal'),
       command=btnClickFunction1).place(x=450, y=108)


# This is the section of code which creates a button
Button(root, text='Set Stock', bg='#FAEBD7', font=('arial', 12, 'normal'),
       command=btnClickFunction2).place(x=350, y=108)


# This is the section of code which creates a button
Button(root, text='Fetch3', bg='#FAEBD7', font=('arial', 12, 'normal'),
       command=btnClickFunction3).place(x=550, y=108)


# This is the section of code which creates a button
Button(root, text='Fetch4', bg='#FAEBD7', font=('arial', 12, 'normal'),
       command=btnClickFunction4).place(x=650, y=108)

root.resizable(False, False)

root.mainloop()
