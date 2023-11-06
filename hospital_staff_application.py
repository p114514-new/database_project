import tkinter as tk
from tkinter import messagebox
from tkinter.ttk import Treeview
import pandas as pd
import sqlite3


def Check_patient_profile(main_window):
    main_window.destroy()
    view_window = tk.Tk()
    view_window.title("View Table")
    from main import setscreen
    setscreen(view_window, 800, 600)
    # Create a connection to the SQLite database
    conn = sqlite3.connect('hospital_database.db')
    cursor = conn.cursor()

    res = cursor.execute(
        "SELECT * FROM Patients ",
    )

    table_data = res.fetchall()
    # Create a tkinter Treeview widget
    treeview = tk.ttk.Treeview(view_window)

    # Create a label for displaying messages
    message_label = tk.Label(view_window)
    conn.close()

    if table_data:
        # Create a pandas DataFrame from the table data
        df = pd.DataFrame(table_data)
        df.columns = [description[0] for description in cursor.description]

        # Destroy and recreate the columns in the Treeview widget
        treeview.destroy()
        treeview = tk.ttk.Treeview(view_window)

        # Create the column headings in the Treeview widget
        table_columns = df.columns
        treeview["columns"] = tuple(table_columns)
        for column in table_columns:
            treeview.heading(column, text=column)
            treeview.column(column, width=100)

        # Insert the table data into the Treeview widget
        for i, row in df.iterrows():
            treeview.insert("", "end", values=tuple(row))
    else:
        # No data returned, display a message
        message_label.config(text="No data available for this table.")
        message_label.pack()

        # No data available, but we can still refresh the column names
        columns = [description[0] for description in cursor.description]
        treeview["columns"] = tuple(columns)
        for column in columns:
            treeview.heading(column, text=column)
            treeview.column(column, width=100)

            # Pack the Treeview widget
    treeview.pack(expand=True, fill=tk.BOTH)

    exit_button = tk.Button(view_window, text="exit", command=lambda: exit_to_entry(view_window))

    exit_button.pack(side=tk.BOTTOM)

    view_window.mainloop()


def Check_doctors(main_window):
    main_window.destroy()
    view_window = tk.Tk()
    view_window.title("View Table")
    # Create a tkinter Treeview widget

    from main import setscreen
    setscreen(view_window, 800, 600)
    # Create a connection to the SQLite database
    conn = sqlite3.connect('hospital_database.db')
    cursor = conn.cursor()

    label_Department_idd = tk.Label(view_window, text="search by department_id :")
    label_Department_idd.pack()
    entry_Department_id = tk.Entry(view_window, width=30)
    entry_Department_id.pack()
    res = cursor.execute(
        "SELECT * FROM Doctors "
    )
    print([description[0] for description in cursor.description])
    des = [description[0] for description in cursor.description]
    print(des)
    treeview = tk.ttk.Treeview(view_window)
    table_data = res.fetchall()
    # Create a label for displaying messages
    message_label = tk.Label(view_window)

    button0 = tk.Button(view_window, text=" search",
                        command=lambda: get_department_id(treeview, res, view_window, entry_Department_id, des))
    button0.pack()
    if table_data:
        # Create a pandas DataFrame from the table data
        df = pd.DataFrame(table_data)
        print(des)
        print(df)
        df.columns = des

        # Destroy and recreate the columns in the Treeview widget
        treeview.destroy()
        treeview = tk.ttk.Treeview(view_window)

        # Create the column headings in the Treeview widget
        table_columns = df.columns
        treeview["columns"] = tuple(table_columns)
        for column in table_columns:
            treeview.heading(column, text=column)
            treeview.column(column, width=100)

        # Insert the table data into the Treeview widget
        for i, row in df.iterrows():
            treeview.insert("", "end", values=tuple(row))
    else:
        # No data returned, display a message
        message_label.config(text="No data available for this table.")
        message_label.pack()

        # No data available, but we can still refresh the column names
        columns = [description[0] for description in cursor.description]
        treeview["columns"] = tuple(columns)
        for column in columns:
            treeview.heading(column, text=column)
            treeview.column(column, width=100)

            # Pack the Treeview widget
    treeview.pack(expand=True, fill=tk.BOTH)
    exit_button = tk.Button(view_window, text="exit", command=lambda: exit_to_entry(view_window))
    exit_button.pack()
    view_window.mainloop()


def get_department_id(treeview, res, view_window, entry_Department_id, des):
    Department_id = entry_Department_id.get()
    conn = sqlite3.connect('hospital_database.db')
    cursor = conn.cursor()
    if Department_id:
        res = cursor.execute(
            "SELECT * FROM Doctors where Doctors.department_id=?", (int(Department_id),)
        )
    else:
        res = cursor.execute(
            "SELECT * FROM Doctors "
        )
    refresh(treeview, res, view_window, des)


##不知道为什么treeview没有刷新
def refresh(treeview, res, view_window, des):
    table_data = res.fetchall()
    # Create a label for displaying messages
    message_label = tk.Label(view_window)
    conn = sqlite3.connect('hospital_database.db')
    cursor = conn.cursor()
    if table_data:
        # Create a pandas DataFrame from the table data
        df = pd.DataFrame(table_data)
        print(cursor.description, 'ds')
        print(df)
        df.columns = des

        # Destroy and recreate the columns in the Treeview widget
        treeview.destroy()
        treeview = tk.ttk.Treeview(view_window)

        # Create the column headings in the Treeview widget
        table_columns = df.columns
        treeview["columns"] = tuple(table_columns)
        for column in table_columns:
            treeview.heading(column, text=column)
            treeview.column(column, width=100)

        # Insert the table data into the Treeview widget
        for i, row in df.iterrows():
            treeview.insert("", "end", values=tuple(row))
    else:
        # No data returned, display a message
        message_label.config(text="No data available for this table.")
        message_label.pack()

        # No data available, but we can still refresh the column names
        columns = [description[0] for description in cursor.description]
        treeview["columns"] = tuple(columns)
        for column in columns:
            treeview.heading(column, text=column)
            treeview.column(column, width=100)
    treeview.pack(expand=True, fill=tk.BOTH)


def logout(main_window):
    main_window.destroy()
    from main import create_login_window
    create_login_window()


def exit_to_entry(window):
    window.destroy()
    hospital_staff_application_entry_window()


def get_row_data(treeview, rows):
    values = []
    for row in rows:
        item_id = treeview.get_children()[row]
        values.append(treeview.item(item_id)['values'])
    return values


def hospital_staff_application_entry_window():
    main_window = tk.Tk()
    main_window.title("Main Application")
    from main import setscreen
    setscreen(main_window, 600, 400)
    # Create four parallel buttons
    button1 = tk.Button(main_window, text="Check_patient_profile", command=lambda: Check_patient_profile(main_window))
    button2 = tk.Button(main_window, text="Check_doctors", command=lambda: Check_doctors(main_window))

    button5 = tk.Button(main_window, text="logout", command=lambda: logout(main_window))
    # Place the buttons vertically
    button1.pack(side=tk.TOP, padx=10, pady=15)
    button2.pack(side=tk.TOP, padx=10, pady=15)
    button5.pack(side=tk.TOP, padx=10, pady=15)
    main_window.mainloop()
