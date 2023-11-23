import tkinter as tk
from tkinter import messagebox
from tkinter.ttk import Treeview
import pandas as pd
import sqlite3


# def Check_patient_profile(main_window):
#     main_window.destroy()
#     view_window = tk.Tk()
#     view_window.title("View Table")
#     from main import setscreen
#     setscreen(view_window, 800, 600)
#     # Create a connection to the SQLite database
#     conn = sqlite3.connect('hospital_database.db')
#     cursor = conn.cursor()
#
#     res = cursor.execute(
#         "SELECT * FROM Patients ",
#     )
#
#     table_data = res.fetchall()
#     # Create a tkinter Treeview widget
#     treeview = tk.ttk.Treeview(view_window)
#
#     # Create a label for displaying messages
#     message_label = tk.Label(view_window)
#     conn.close()
#
#     if table_data:
#         # Create a pandas DataFrame from the table data
#         df = pd.DataFrame(table_data)
#         df.columns = [description[0] for description in cursor.description]
#
#         # Destroy and recreate the columns in the Treeview widget
#         treeview.destroy()
#         treeview = tk.ttk.Treeview(view_window)
#
#         # Create the column headings in the Treeview widget
#         table_columns = df.columns
#         treeview["columns"] = tuple(table_columns)
#         for column in table_columns:
#             treeview.heading(column, text=column)
#             treeview.column(column, width=100)
#
#         # Insert the table data into the Treeview widget
#         for i, row in df.iterrows():
#             treeview.insert("", "end", values=tuple(row))
#     else:
#         # No data returned, display a message
#         message_label.config(text="No data available for this table.")
#         message_label.pack()
#
#         # No data available, but we can still refresh the column names
#         columns = [description[0] for description in cursor.description]
#         treeview["columns"] = tuple(columns)
#         for column in columns:
#             treeview.heading(column, text=column)
#             treeview.column(column, width=100)
#
#             # Pack the Treeview widget
#     treeview.pack(expand=True, fill=tk.BOTH)
#
#     exit_button = tk.Button(view_window, text="exit", command=lambda: exit_to_entry(view_window))
#
#     exit_button.pack(side=tk.BOTTOM)
#
#     view_window.mainloop()
#
#
# def Check_doctors(main_window):
#     main_window.destroy()
#     view_window = tk.Tk()
#     view_window.title("View Table")
#     # Create a tkinter Treeview widget
#
#     from main import setscreen
#     setscreen(view_window, 800, 600)
#     # Create a connection to the SQLite database
#     conn = sqlite3.connect('hospital_database.db')
#     cursor = conn.cursor()
#
#     label_Department_idd = tk.Label(view_window, text="search by department_id :")
#     label_Department_idd.pack()
#     entry_Department_id = tk.Entry(view_window, width=30)
#     entry_Department_id.pack()
#     res = cursor.execute(
#         "SELECT * FROM Doctors "
#     )
#     print([description[0] for description in cursor.description])
#     des = [description[0] for description in cursor.description]
#     print(des)
#     treeview = tk.ttk.Treeview(view_window)
#     table_data = res.fetchall()
#     # Create a label for displaying messages
#     message_label = tk.Label(view_window)
#
#     button0 = tk.Button(view_window, text=" search",
#                         command=lambda: get_department_id(treeview, res, view_window, entry_Department_id, des))
#     button0.pack()
#     if table_data:
#         # Create a pandas DataFrame from the table data
#         df = pd.DataFrame(table_data)
#         print(des)
#         print(df)
#         df.columns = des
#
#         # Destroy and recreate the columns in the Treeview widget
#         treeview.destroy()
#         treeview = tk.ttk.Treeview(view_window)
#
#         # Create the column headings in the Treeview widget
#         table_columns = df.columns
#         treeview["columns"] = tuple(table_columns)
#         for column in table_columns:
#             treeview.heading(column, text=column)
#             treeview.column(column, width=100)
#
#         # Insert the table data into the Treeview widget
#         for i, row in df.iterrows():
#             treeview.insert("", "end", values=tuple(row))
#     else:
#         # No data returned, display a message
#         message_label.config(text="No data available for this table.")
#         message_label.pack()
#
#         # No data available, but we can still refresh the column names
#         columns = [description[0] for description in cursor.description]
#         treeview["columns"] = tuple(columns)
#         for column in columns:
#             treeview.heading(column, text=column)
#             treeview.column(column, width=100)
#
#             # Pack the Treeview widget
#     treeview.pack(expand=True, fill=tk.BOTH)
#     exit_button = tk.Button(view_window, text="exit", command=lambda: exit_to_entry(view_window))
#     exit_button.pack()
#     view_window.mainloop()


# def get_department_id(treeview, res, view_window, entry_Department_id, des):
#     Department_id = entry_Department_id.get()
#     conn = sqlite3.connect('hospital_database.db')
#     cursor = conn.cursor()
#     if Department_id:
#         res = cursor.execute(
#             "SELECT * FROM Doctors where Doctors.department_id=?", (int(Department_id),)
#         )
#     else:
#         res = cursor.execute(
#             "SELECT * FROM Doctors "
#         )
#     refresh(treeview, res, view_window, des)
#
#
# ##不知道为什么treeview没有刷新
# def refresh(treeview, res, view_window, des):
#     table_data = res.fetchall()
#     # Create a label for displaying messages
#     message_label = tk.Label(view_window)
#     conn = sqlite3.connect('hospital_database.db')
#     cursor = conn.cursor()
#     if table_data:
#         # Create a pandas DataFrame from the table data
#         df = pd.DataFrame(table_data)
#         print(cursor.description, 'ds')
#         print(df)
#         df.columns = des
#
#         # Destroy and recreate the columns in the Treeview widget
#         treeview.destroy()
#         treeview = tk.ttk.Treeview(view_window)
#
#         # Create the column headings in the Treeview widget
#         table_columns = df.columns
#         treeview["columns"] = tuple(table_columns)
#         for column in table_columns:
#             treeview.heading(column, text=column)
#             treeview.column(column, width=100)
#
#         # Insert the table data into the Treeview widget
#         for i, row in df.iterrows():
#             treeview.insert("", "end", values=tuple(row))
#
#     else:
#         # No data returned, display a message
#         message_label.config(text="No data available for this table.")
#         message_label.pack()
#
#         # No data available, but we can still refresh the column names
#         columns = [description[0] for description in cursor.description]
#         treeview["columns"] = tuple(columns)
#         for column in columns:
#             treeview.heading(column, text=column)
#             treeview.column(column, width=100)
#     treeview.pack(expand=True, fill=tk.BOTH)
#

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
def search_views(treeview, table, search_entry, search_column):
    conn = sqlite3.connect('hospital_database.db')
    cursor = conn.cursor()

    name = search_entry.get().strip()  # Get the entered doctor's name
    try:
     if name == "":
        # If the search entry is empty, query the entire Doctors table
        cursor.execute(f"SELECT * FROM {table}")
     else:
        # Otherwise, search for the entered doctor's name
        cursor.execute("SELECT * FROM " + table + " WHERE " + search_column[table] + " LIKE ?", ('%' + name + '%',))
    except:
        messagebox.showerror("Error", "Wrong input")
    search_results = cursor.fetchall()
    conn.close()

    # Clear the Treeview
    treeview.delete(*treeview.get_children())

    # Insert data into the Treeview
    for i, row in enumerate(search_results, start=1):
        # Add 'I' prefix and zero-padding to the index
        index = 'I' + str(i).zfill(3)
        treeview.insert("", "end", iid=index, values=row)
def filter_views(treeview, table, search_entry, myfilter):
    conn = sqlite3.connect('hospital_database.db')
    cursor = conn.cursor()
    try:
       filt = int(search_entry.get())
    except:
       filt = search_entry.get()
    # Get the entered doctor's name
    try:
     if not filt:
        # If the search entry is empty, query the entire Doctors table
        cursor.execute(f"SELECT * FROM {table}")
     else:
        # Otherwise, search for the entered doctor's name
        cursor.execute("SELECT * FROM " + table + " WHERE " + myfilter+ " = ?", (filt,))
    except Exception as e:
        messagebox.showerror("Error", "Wrong input")
        print(e)
    search_results = cursor.fetchall()
    conn.close()

    # Clear the Treeview
    treeview.delete(*treeview.get_children())

    # Insert data into the Treeview
    for i, row in enumerate(search_results, start=1):
        # Add 'I' prefix and zero-padding to the index
        index = 'I' + str(i).zfill(3)
        treeview.insert("", "end", iid=index, values=row)
def refresh_treeview(treeview, table: str):
    # Clear existing data in the Treeview
    treeview.delete(*treeview.get_children())

    # Create a connection to the SQLite database
    conn = sqlite3.connect('hospital_database.db')
    cursor = conn.cursor()

    # Retrieve the data from the Buffer1 table
    cursor.execute("SELECT * FROM " + table)
    buffer1_data = cursor.fetchall()

    conn.close()

    # Insert data into the Treeview
    for i, row in enumerate(buffer1_data, start=1):
        # Add 'I' prefix and zero-padding to the index
        index = 'I' + str(i).zfill(3)
        treeview.insert("", "end", iid=index, values=row)

def view_tables(main_window):
    main_window.destroy()
    view_window = tk.Tk()
    view_window.title("View Table")
    from main import setscreen
    setscreen(view_window, 800, 600)

    # Create a connection to the SQLite database
    conn = sqlite3.connect('hospital_database.db')
    cursor = conn.cursor()

    # Retrieve the available tables from the database schema
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
    tables = cursor.fetchall()

    conn.close()

    # Remove the buffer tables from the options list
    options = ['Patients','Doctors','Departments']

    # Create a search module
    search_frame = tk.Frame(view_window)
    name_for_search_frame = {'Patients': 'Patient Name', 'Departments': 'Department Name', 'Doctors': 'Doctor Name',
                             'Hospital_Staff': 'Staff Name', 'Nurses': 'Nurse Name', 'Rooms': 'Room id',
                             'Nurse_Patient_Room': 'Patient id', 'Treatments': 'Patient id'
                             }
    search_column = {'Patients': 'patient_name', 'Departments': 'department_name', 'Doctors': 'doctor_name',
                     'Hospital_Staff': 'staff_name', 'Nurses': 'nurse_name', 'Rooms': 'room_id',
                     'Nurse_Patient_Room': 'patient_id', 'Treatments': 'patient_id'
                     }
    search_label = tk.Label(search_frame, text=f"Search for {name_for_search_frame[options[0]]}: ")
    search_entry = tk.Entry(search_frame)
    search_button = tk.Button(search_frame, text="Search",
                              command=lambda: search_views(treeview, options[0], search_entry, search_column))
    default_button = tk.Button(search_frame, text="Default", command=lambda: refresh_treeview(treeview, options[0]))

    # print(options)
    # Pack the search module
    search_frame.pack(pady=10)
    search_label.grid(row=0, column=0)
    search_entry.grid(row=0, column=1,padx=5)
    search_button.grid(row=0, column=2)
    default_button.grid(row=0, column=3,padx=5)

    filter_label = tk.Label(search_frame, text=f"Filtered by Department_id: ")
    filter_entry = tk.Entry(search_frame)
    filter_button = tk.Button(search_frame, text="Filter",
                              command=lambda: filter_views(treeview, 'Doctors', filter_entry, 'department_id'))
    filter_default_button = tk.Button(search_frame, text="Default", command=lambda: refresh_treeview(treeview, "Doctors"))



    # Create a tkinter Treeview widget
    treeview = tk.ttk.Treeview(view_window)

    # Create a label for displaying messages
    message_label = tk.Label(view_window)

    def on_selection_changed(selection):
        nonlocal treeview, message_label

        search_label.config(text=f"Search for {name_for_search_frame[selection]}: ")
        search_button.config(command=lambda: search_views(treeview, selection, search_entry, search_column))
        default_button.config(command=lambda: refresh_treeview(treeview, selection))
        if selection=="Doctors":
            filter_label.grid(row=1, column=0)
            filter_entry.grid(row=1, column=1,padx=5)
            filter_button.grid(row=1, column=2)
            filter_default_button.grid(row=1, column=3,padx=5)
        else:
            filter_label.pack_forget()
            filter_entry.pack_forget()
            filter_button.pack_forget()
            filter_default_button.pack_forget()
        # Clear any previous data in the Treeview widget
        treeview.delete(*treeview.get_children())

        # Remove the message label if it exists
        message_label.pack_forget()

        # Create a connection to the SQLite database
        conn = sqlite3.connect('hospital_database.db')
        cursor = conn.cursor()

        # Execute a SELECT query to retrieve data from the selected table
        cursor.execute(f"SELECT * FROM {selection}")
        table_data = cursor.fetchall()

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
            treeview["show"] = "headings"
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

    # Create the OptionMenu widget
    selected_table = tk.StringVar(view_window)
    selected_table.set(options[0])
    option_menu = tk.OptionMenu(view_window, selected_table, *options, command=on_selection_changed)
    option_menu.pack()

    # Execute the initial selection change to display the default table data
    on_selection_changed(selected_table.get())

    exit_button = tk.Button(view_window, text="exit", command=lambda: exit_to_entry(view_window))

    exit_button.pack(side=tk.BOTTOM)

    view_window.mainloop()


def hospital_staff_application_entry_window():
    main_window = tk.Tk()
    main_window.title("Main Application")


    from main import setscreen
    setscreen(main_window, 600, 400)


    # Create four parallel buttons
    button1 = tk.Button(main_window, text="View tables", command=lambda: view_tables(main_window))

    button5 = tk.Button(main_window, text="logout", command=lambda: logout(main_window))


    # Place the buttons vertically
    button1.pack(side=tk.TOP, padx=10, pady=15)

    button5.pack(side=tk.TOP, padx=10, pady=15)
    main_window.mainloop()
