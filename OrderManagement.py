# MySQL Library to connect database
import mysql.connector
# Tkinter library for GUI
from tkinter import *
# Pandas library for dataframe
import pandas as pd
# PandasTable for table
from pandastable import Table, TableModel


# Establish database connection
conn = mysql.connector.connect(
    host="localhost", user="root", password="", database="ordermanagement")
# Cursor to run queries
cursor = conn.cursor()

# function to call on click for menu option


def OptionMenu_SelectionEvent(*args):
    option = variable.get()
# calling SQL queries according to option selected
    if (option == "Get List of customers with their payments"):
        cursor.execute(
            "SELECT c.customerName, SUM(p.amount) AS amount FROM payments p, customers c WHERE p.customerNumber = c.customerNumber GROUP BY p.customerNumber")
    elif (option == "List customer with median payment"):
        cursor.execute("SET @rowindex := -1")
        cursor.execute("SELECT customerName, contactLastName, phone FROM customers WHERE customerNumber = (SELECT customerNumber FROM payments WHERE amount = (SELECT AVG(a.amount) as Median FROM (SELECT @rowindex:=@rowindex + 1 AS rowindex,payments.amount AS amount FROM payments ORDER BY payments.amount) AS a WHERE a.rowindex IN (FLOOR(@rowindex / 2), CEIL(@rowindex / 2))))")
    elif (option == "List payments greater than average"):
        cursor.execute(
            "SELECT * FROM payments WHERE amount > (SELECT AVG(amount) FROM payments)")
    elif (option == "List customers who cancelled order"):
        cursor.execute(
            "SELECT * FROM customers WHERE customerNumber IN (SELECT DISTINCT customerNumber FROM orders WHERE status = \"Cancelled\")")
    elif (option == "List customers whom orders are on hold"):
        cursor.execute(
            "SELECT * FROM customers WHERE customerNumber IN (SELECT customerNumber FROM orders WHERE status = \"On Hold\")")
# fetching all results
    values = cursor.fetchall()
# getting column names
    columns = [col[0] for col in cursor.description]
# Creating dataframe
    df = pd.DataFrame(values, columns=columns)
    df.head()
# Creating frame for table
    f = Frame(gui)
    # f.pack(fill=BOTH,expand=1)
# creating table with dataframe and adding it to frame
    table = pt = Table(f, dataframe=df, showtoolbar=True, showstatusbar=True)
    pt.show()
    f.grid(row=3, column=0)


# List for options
OPTIONS = [
    "Get List of customers with their payments",
    "List customer with median payment",
    "List payments greater than average",
    "List customers who cancelled order",
    "List customers whom orders are on hold"
]

# GUI root for adding widgets
gui = Tk()
# Setting title
gui.title("Order Management System")
# Setting Geometry size
gui.geometry("650x600")

l = Label(gui, text="Order Management System")
l.config(font=("Courier", 32))
l.grid(row=0, column=0)

l = Label(gui, text="Please Select an option from menu below")
l.config(font=("Courier", 18))
l.grid(row=1, column=0)

variable = StringVar(gui)
variable.set(OPTIONS[0])

w = OptionMenu(gui, variable, *OPTIONS, command=OptionMenu_SelectionEvent)
w.config(font=("Courier", 14))
w.grid(row=2, column=0)

# to display screen
gui.mainloop()

# close database connection
conn.close()
