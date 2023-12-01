import sqlite3
import tkinter as tk
from collections import defaultdict
from tkinter import messagebox
import tkinter.simpledialog as simpledialog
from tkinter.ttk import Treeview

import pandas as pd


def get_all_attributes():
    # query to get all table names
    query = "SELECT name FROM sqlite_master WHERE type='table';"
    conn = sqlite3.connect('hospital_database.db')
    cursor = conn.cursor()
    cursor.execute(query)
    tables = cursor.fetchall()

    # for each table, get all column names
    all_attributes = {}
    for table in tables:
        query = f"PRAGMA table_info({table[0]});"
        cursor.execute(query)
        attributes = cursor.fetchall()
        attributes = [attribute[1] for attribute in attributes]
        all_attributes[table[0]] = attributes

    conn.close()

    return all_attributes


def exit_to_entry(window):
    window.destroy()
    admin_application_entry_window()


def get_row_data(treeview, rows):
    values = []
    for row in rows:
        item_id = treeview.get_children()[row]
        values.append(treeview.item(item_id)['values'])
    return values


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


def confirm_buffer_1(treeview):
    selected_items = treeview.selection()  # Get the selected items
    print(selected_items)

    if selected_items:
        selected_lines = [int(x[1:]) - 1 for x in selected_items]
        selected_data = get_row_data(treeview, selected_lines)
        print(selected_data)

        # Create a connection to the SQLite database
        conn = sqlite3.connect('hospital_database.db')
        cursor = conn.cursor()

        try:
            # Update the change_status column to '+'
            for row in selected_data:
                doctor_id = row[0]
                cursor.execute("UPDATE Buffer1 SET change_status = '+' WHERE doctor_id = ?", (doctor_id,))

                if row[3] != '+':
                    # Enable foreign key constraints
                    conn.execute('PRAGMA foreign_keys = ON')

                    cursor.execute(
                        "INSERT INTO Doctors (doctor_id, doctor_name, department_id) VALUES (?,?,?)", row[:-1])

            conn.commit()
            messagebox.showinfo("Confirm", "Selected rows confirmed successfully.")

            refresh_treeview(treeview, 'Buffer1')
        except Exception as e:
            messagebox.showerror("Error", f"Error occurred while confirming rows: {str(e)}")
        finally:
            conn.close()
    else:
        messagebox.showinfo("Confirm", "Please select a row to confirm.")


def confirm_buffer_2(treeview):
    selected_items = treeview.selection()  # Get the selected items
    print(selected_items)

    if selected_items:
        selected_lines = [int(x[1:]) - 1 for x in selected_items]
        selected_data = get_row_data(treeview, selected_lines)
        print(selected_data)

        # Create a connection to the SQLite database
        conn = sqlite3.connect('hospital_database.db')
        cursor = conn.cursor()

        try:
            # Update the change_status column to '+'
            for row in selected_data:
                deparment_id = row[0]
                cursor.execute("UPDATE Buffer2 SET change_status = '+' WHERE department_id = ?", (deparment_id,))

                if row[2] != '+':
                    # Enable foreign key constraints
                    conn.execute('PRAGMA foreign_keys = ON')

                    cursor.execute(
                        "INSERT INTO Departments (department_id, department_name) VALUES (?,?)", row[:-1])

            conn.commit()
            messagebox.showinfo("Confirm", "Selected rows confirmed successfully.")

            refresh_treeview(treeview, 'Buffer2')
        except Exception as e:
            messagebox.showerror("Error", f"Error occurred while confirming rows: {str(e)}")
        finally:
            conn.close()
    else:
        messagebox.showinfo("Confirm", "Please select a row to confirm.")


def deny_buffer_1(treeview):
    selected_items = treeview.selection()  # Get the selected items

    if selected_items:
        selected_lines = [int(x[1:]) - 1 for x in selected_items]
        selected_data = get_row_data(treeview, selected_lines)

        # Create a connection to the SQLite database
        conn = sqlite3.connect('hospital_database.db')
        cursor = conn.cursor()

        try:
            # Update the change_status column to '-'
            for row in selected_data:
                doctor_id = row[0]
                cursor.execute("UPDATE Buffer1 SET change_status = '-' WHERE doctor_id = ?", (doctor_id,))

                if row[3] != '-':
                    # Enable foreign key constraints
                    conn.execute('PRAGMA foreign_keys = ON')

                    cursor.execute(
                        "DELETE FROM Doctors WHERE doctor_id = ? AND doctor_name = ? AND department_id = ?", row[:-1])

            conn.commit()
            messagebox.showinfo("Deny", "Selected rows denied successfully.")

            refresh_treeview(treeview, 'Buffer1')
        except Exception as e:
            messagebox.showerror("Error", f"Error occurred while denying rows: {str(e)}")
        finally:
            conn.close()
    else:
        messagebox.showinfo("Deny", "Please select a row to deny.")


def deny_buffer_2(treeview):
    selected_items = treeview.selection()  # Get the selected items

    if selected_items:
        selected_lines = [int(x[1:]) - 1 for x in selected_items]
        selected_data = get_row_data(treeview, selected_lines)

        # Create a connection to the SQLite database
        conn = sqlite3.connect('hospital_database.db')
        cursor = conn.cursor()

        try:
            # Update the change_status column to '-'
            for row in selected_data:
                department_id = row[0]
                cursor.execute("UPDATE Buffer2 SET change_status = '-' WHERE department_id = ?", (department_id,))

                if row[2] != '-':
                    # Enable foreign key constraints
                    conn.execute('PRAGMA foreign_keys = ON')

                    cursor.execute(
                        "DELETE FROM Departments WHERE department_id = ? AND department_name = ?", row[:-1])

            conn.commit()
            messagebox.showinfo("Deny", "Selected rows denied successfully.")

            refresh_treeview(treeview, 'Buffer2')
        except Exception as e:
            messagebox.showerror("Error", f"Error occurred while denying rows: {str(e)}")
        finally:
            conn.close()
    else:
        messagebox.showinfo("Deny", "Please select a row to deny.")


def search_views(treeview, table, search_entry, search_column):
    conn = sqlite3.connect('hospital_database.db')
    cursor = conn.cursor()

    name = search_entry.get().strip()  # Get the entered doctor's name

    if name == "":
        # If the search entry is empty, query the entire Doctors table
        cursor.execute(f"SELECT * FROM {table}")
    else:
        # Otherwise, search for the entered doctor's name
        cursor.execute("SELECT * FROM " + table + " WHERE " + search_column[table] + " LIKE ?", ('%' + name + '%',))

    search_results = cursor.fetchall()
    conn.close()

    # Clear the Treeview
    treeview.delete(*treeview.get_children())

    # Insert data into the Treeview
    for i, row in enumerate(search_results, start=1):
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
    options = [table[0] for table in tables if table[0] not in ["Buffer1", "Buffer2"]]

    # Create a search module
    search_frame = tk.Frame(view_window)
    name_for_search_frame = {'Patients': 'Patient Name', 'Departments': 'Department Name', 'Doctors': 'Doctor Name',
                             'Hospital_Staff': 'Staff Name', 'Nurses': 'Nurse Name', 'Rooms': 'Room id',
                             'Nurse_Patient_Room': 'Patient id', 'Treatments': 'Patient id', 'Login': 'Username'
                             }
    search_column = {'Patients': 'patient_name', 'Departments': 'department_name', 'Doctors': 'doctor_name',
                     'Hospital_Staff': 'staff_name', 'Nurses': 'nurse_name', 'Rooms': 'room_id',
                     'Nurse_Patient_Room': 'patient_id', 'Treatments': 'patient_id', 'Login': 'username'
                     }
    search_label = tk.Label(search_frame, text=f"Search for {name_for_search_frame[options[0]]}: ")
    search_entry = tk.Entry(search_frame)
    search_button = tk.Button(search_frame, text="Search",
                              command=lambda: search_views(treeview, options[0], search_entry, search_column))
    default_button = tk.Button(search_frame, text="Default", command=lambda: refresh_treeview(treeview, options[0]))

    # Pack the search module
    search_frame.pack(pady=10)
    search_label.pack(side=tk.LEFT)
    search_entry.pack(side=tk.LEFT, padx=5)
    search_button.pack(side=tk.LEFT)
    default_button.pack(side=tk.LEFT, padx=5)

    # Create a tkinter Treeview widget
    treeview = tk.ttk.Treeview(view_window)

    # Create a label for displaying messages
    message_label = tk.Label(view_window)

    def on_selection_changed(selection):
        nonlocal treeview, message_label

        search_label.config(text=f"Search for {name_for_search_frame[selection]}: ")
        search_button.config(command=lambda: search_views(treeview, selection, search_entry, search_column))
        default_button.config(command=lambda: refresh_treeview(treeview, selection))

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


def SelectItem(event, treeview, table_name):
    print(get_all_attributes())
    curItem = treeview.item(treeview.focus())
    col = treeview.identify_column(event.x)
    print('curItem = ', curItem)
    print('col = ', col)

    if col == '#0':
        cell_value = curItem['text']
    else:
        cell_value = curItem['values'][int(col[1:]) - 1]
    print('cell_value = ', cell_value)

    new_value = prompt_for_value(cell_value)

    column_name = treeview.heading(int(col[1:]) - 1)['text']
    primary_keys = {'Patients': ['patient_id'], 'Departments': ['department_id'], 'Doctors': ['doctor_id'],
                    'Hospital_Staff': ['staff_id'], 'Nurses': ['nurse_id'], 'Rooms': ['room_id'],
                    'Nurse_Patient_Room': ['patient_id', 'room_id'], 'Treatments': ['treatment_id'],
                    'Login': ['realname', 'password']
                    }

    if new_value is not None:
        update_value(treeview, curItem['values'], new_value, table_name, column_name, primary_keys)


def prompt_for_value(old_value):
    new_value = simpledialog.askstring("Modify Value", "Enter the new value:", initialvalue=old_value)
    return new_value


def update_value(treeview, values, new_value, table_name, column_name, primary_keys):
    conn = sqlite3.connect('hospital_database.db')
    cursor = conn.cursor()

    # Check if the column is a primary key
    if is_key(table_name, column_name, primary_keys) == 1:
        messagebox.showwarning("Invalid Operation", "Modifying primary keys is not allowed.")
        return
    elif is_key(table_name, column_name, primary_keys) == 2:
        # list the appearance of the foreign key in all tables
        column_names = get_all_attributes()
        tables_having_this_key = [x for x in column_names if
                                  column_name in column_names[x] and x not in ['Buffer1', 'Buffer2']]
        result = messagebox.askquestion("Dangerous Operation",
                                        "Modifying foreign keys is a dangerous approach. \n" +
                                        "All tables having this key are: " + str(tables_having_this_key) +
                                        "\nDo you want to continue? The system will only modify this cell but will not " +
                                        "do further modifications in other tables. " +
                                        "Make sure all values for this foreign key are consistent.",
                                        icon='warning',
                                        type='yesno')

        if result == 'no':
            return

    # Check if the new value is valid
    if not is_valid_value(column_name, new_value):
        messagebox.showwarning("Invalid Value", "The entered value is not valid.")
        return

    # Construct the UPDATE query
    query = f"UPDATE {table_name} SET {column_name} = ? WHERE "

    # add the priamry key condition to the query
    for i in range(len(primary_keys[table_name])):
        query += f"{primary_keys[table_name][i]} = ?"
        if i != len(primary_keys[table_name]) - 1:
            query += " AND "
    # get the primary key values for the selected row
    primary_key_values = []
    for i in range(len(primary_keys[table_name])):
        primary_key_values.append(values[i])

    try:
        cursor.execute(query, (new_value, *primary_key_values))
        conn.commit()
        messagebox.showinfo("Value Updated", "The value has been successfully updated.")
    except sqlite3.Error as e:
        messagebox.showerror("Database Error", str(e))
    finally:
        conn.close()

    # Refresh the Treeview widget
    refresh_treeview(treeview, table_name)


def is_key(table_name, column_name, primary_keys):
    foreign_keys = defaultdict(list)
    foreign_keys['Patients'] = ['room_id']
    foreign_keys['Doctors'] = ['department_id']
    foreign_keys['Treatments'] = ['room_id']
    foreign_keys['Nurse_Patient_Room'] = ['room_id']
    if column_name in primary_keys[table_name]:
        return 1
    elif column_name in foreign_keys[table_name]:
        return 2
    else:
        return 0


def is_valid_value(column_name, new_value):
    # Implement the logic to check if the new value is valid for the column
    # Replace with your own implementation
    pass
    return True


def modify_tables_interface(main_window):
    main_window.destroy()
    modifying_interface = tk.Tk()
    modifying_interface.title("Modify Table")
    from main import setscreen
    setscreen(modifying_interface, 800, 600)

    # Create a connection to the SQLite database
    conn = sqlite3.connect('hospital_database.db')
    cursor = conn.cursor()

    # Retrieve the available tables from the database schema
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
    tables = cursor.fetchall()

    conn.close()

    # Remove the buffer tables from the options list
    options = [table[0] for table in tables if table[0] not in ["Buffer1", "Buffer2"]]

    # Create a search module
    search_frame = tk.Frame(modifying_interface)
    name_for_search_frame = {'Patients': 'Patient Name', 'Departments': 'Department Name', 'Doctors': 'Doctor Name',
                             'Hospital_Staff': 'Staff Name', 'Nurses': 'Nurse Name', 'Rooms': 'Room id',
                             'Nurse_Patient_Room': 'Patient id', 'Treatments': 'Patient id', 'Login': 'Username'
                             }
    search_column = {'Patients': 'patient_name', 'Departments': 'department_name', 'Doctors': 'doctor_name',
                     'Hospital_Staff': 'staff_name', 'Nurses': 'nurse_name', 'Rooms': 'room_id',
                     'Nurse_Patient_Room': 'patient_id', 'Treatments': 'patient_id', 'Login': 'username'
                     }
    search_label = tk.Label(search_frame, text=f"Search for {name_for_search_frame[options[0]]}: ")
    search_entry = tk.Entry(search_frame)
    search_button = tk.Button(search_frame, text="Search",
                              command=lambda: search_views(treeview, options[0], search_entry, search_column))
    default_button = tk.Button(search_frame, text="Default", command=lambda: refresh_treeview(treeview, options[0]))

    # Pack the search module
    search_frame.pack(pady=10)
    search_label.pack(side=tk.LEFT)
    search_entry.pack(side=tk.LEFT, padx=5)
    search_button.pack(side=tk.LEFT)
    default_button.pack(side=tk.LEFT, padx=5)

    # Create a tkinter Treeview widget
    treeview = tk.ttk.Treeview(modifying_interface)

    # Create a label for displaying messages
    message_label = tk.Label(modifying_interface)

    def on_selection_changed(selection):
        nonlocal treeview, message_label

        search_label.config(text=f"Search for {name_for_search_frame[selection]}: ")
        search_button.config(command=lambda: search_views(treeview, selection, search_entry, search_column))
        default_button.config(command=lambda: refresh_treeview(treeview, selection))

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
            treeview = tk.ttk.Treeview(modifying_interface)

            # Create the column headings in the Treeview widget
            table_columns = df.columns
            treeview["columns"] = tuple(table_columns)
            treeview["show"] = "headings"
            for column in table_columns:
                treeview.heading(column, text=column)
                treeview.column(column, width=100)
                treeview.bind('<ButtonRelease-1>', lambda event: SelectItem(event, treeview, selection))

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
    selected_table = tk.StringVar(modifying_interface)
    selected_table.set(options[0])
    option_menu = tk.OptionMenu(modifying_interface, selected_table, *options, command=on_selection_changed)
    option_menu.pack()

    # Execute the initial selection change to display the default table data
    on_selection_changed(selected_table.get())

    exit_button = tk.Button(modifying_interface, text="exit", command=lambda: exit_to_entry(modifying_interface))

    exit_button.pack(side=tk.BOTTOM)

    modifying_interface.mainloop()


def search_doctors(treeview, search_entry):
    conn = sqlite3.connect('hospital_database.db')
    cursor = conn.cursor()

    doctor_name = search_entry.get().strip()  # Get the entered doctor's name

    if doctor_name == "":
        # If the search entry is empty, query the entire Doctors table
        cursor.execute("SELECT * FROM Buffer1")
    else:
        # Otherwise, search for the entered doctor's name
        cursor.execute("SELECT * FROM Buffer1 WHERE doctor_name LIKE ?", ('%' + doctor_name + '%',))

    search_results = cursor.fetchall()
    conn.close()

    # Clear the Treeview
    treeview.delete(*treeview.get_children())

    # Insert data into the Treeview
    for i, row in enumerate(search_results, start=1):
        # Add 'I' prefix and zero-padding to the index
        index = 'I' + str(i).zfill(3)
        treeview.insert("", "end", iid=index, values=row)


def confirm_doctors_info(main_window):
    main_window.destroy()
    view_window = tk.Tk()
    view_window.title("Confirm Doctor Table Info")
    from main import setscreen
    setscreen(view_window, 800, 600)

    # Create a search module
    search_frame = tk.Frame(view_window)
    search_label = tk.Label(search_frame, text="Search for Doctor's Name: ")
    search_entry = tk.Entry(search_frame)
    search_button = tk.Button(search_frame, text="Search", command=lambda: search_doctors(treeview, search_entry))
    default_button = tk.Button(search_frame, text="Default", command=lambda: refresh_treeview(treeview, 'Buffer1'))

    # Pack the search module
    search_frame.pack(pady=10)
    search_label.pack(side=tk.LEFT)
    search_entry.pack(side=tk.LEFT, padx=5)
    search_button.pack(side=tk.LEFT)
    default_button.pack(side=tk.LEFT, padx=5)

    # Create a connection to the SQLite database
    conn = sqlite3.connect('hospital_database.db')
    cursor = conn.cursor()

    # Retrieve the data from the Buffer1 table
    cursor.execute("SELECT * FROM Buffer1")
    buffer1_data = cursor.fetchall()

    # Get column names from cursor description
    column_names = [description[0] for description in cursor.description]

    conn.close()

    # Create a Treeview widget to display the data
    treeview = Treeview(view_window, show="headings")
    treeview['columns'] = tuple(column_names)  # Set the column names as the column identifiers

    # Configure column headings
    for i, column_name in enumerate(column_names):
        treeview.heading(column_name, text=column_name)

    # Insert data into the Treeview
    for row in buffer1_data:
        treeview.insert("", "end", values=row)

    # Pack the Treeview widget
    treeview.pack(fill=tk.BOTH, expand=True)

    # Create buttons
    button1 = tk.Button(view_window, text="Confirm", width=10, height=2, command=lambda: confirm_buffer_1(treeview))
    button2 = tk.Button(view_window, text="Deny", width=10, height=2, command=lambda: deny_buffer_1(treeview))
    button3 = tk.Button(view_window, text="exit", width=10, height=2, command=lambda: exit_to_entry(view_window))

    # Pack the buttons horizontally at the bottom
    button1.pack(side=tk.LEFT, padx=10, pady=15)
    button2.pack(side=tk.LEFT, padx=10, pady=15)
    button3.pack(side=tk.LEFT, padx=10, pady=15)

    view_window.mainloop()


def search_departments(treeview, search_entry):
    conn = sqlite3.connect('hospital_database.db')
    cursor = conn.cursor()

    department_name = search_entry.get().strip()  # Get the entered doctor's name

    if department_name == "":
        # If the search entry is empty, query the entire Doctors table
        cursor.execute("SELECT * FROM Buffer2")
    else:
        # Otherwise, search for the entered doctor's name
        cursor.execute("SELECT * FROM Buffer2 WHERE Buffer2.department_name LIKE ?", ('%' + department_name + '%',))

    search_results = cursor.fetchall()
    conn.close()

    # Clear the Treeview
    treeview.delete(*treeview.get_children())

    # Insert data into the Treeview
    for i, row in enumerate(search_results, start=1):
        # Add 'I' prefix and zero-padding to the index
        index = 'I' + str(i).zfill(3)
        treeview.insert("", "end", iid=index, values=row)


def confirm_departments_info(main_window):
    main_window.destroy()
    view_window = tk.Tk()
    view_window.title("Confirm Department Table Info")
    from main import setscreen
    setscreen(view_window, 800, 600)

    # Create a search module
    search_frame = tk.Frame(view_window)
    search_label = tk.Label(search_frame, text="Search for Department's Name: ")
    search_entry = tk.Entry(search_frame)
    search_button = tk.Button(search_frame, text="Search", command=lambda: search_departments(treeview, search_entry))
    default_button = tk.Button(search_frame, text="Default", command=lambda: refresh_treeview(treeview, 'Buffer2'))

    # Pack the search module
    search_frame.pack(pady=10)
    search_label.pack(side=tk.LEFT)
    search_entry.pack(side=tk.LEFT, padx=5)
    search_button.pack(side=tk.LEFT)
    default_button.pack(side=tk.LEFT, padx=5)

    # Create a connection to the SQLite database
    conn = sqlite3.connect('hospital_database.db')
    cursor = conn.cursor()

    # Retrieve the data from the Buffer1 table
    cursor.execute("SELECT * FROM Buffer2")
    buffer2_data = cursor.fetchall()

    # Get column names from cursor description
    column_names = [description[0] for description in cursor.description]

    conn.close()

    # Create a Treeview widget to display the data
    treeview = Treeview(view_window, show="headings")
    treeview['columns'] = tuple(column_names)  # Set the column names as the column identifiers

    # Configure column headings
    for i, column_name in enumerate(column_names):
        treeview.heading(column_name, text=column_name)

    # Insert data into the Treeview
    for row in buffer2_data:
        treeview.insert("", "end", values=row)

    # Pack the Treeview widget
    treeview.pack(fill=tk.BOTH, expand=True)

    # Create buttons
    button1 = tk.Button(view_window, text="Confirm", width=10, height=2, command=lambda: confirm_buffer_2(treeview))
    button2 = tk.Button(view_window, text="Deny", width=10, height=2, command=lambda: deny_buffer_2(treeview))
    button3 = tk.Button(view_window, text="exit", width=10, height=2, command=lambda: exit_to_entry(view_window))

    # Pack the buttons horizontally at the bottom
    button1.pack(side=tk.LEFT, padx=10, pady=15)
    button2.pack(side=tk.LEFT, padx=10, pady=15)
    button3.pack(side=tk.LEFT, padx=10, pady=15)

    view_window.mainloop()


def query_by_SQL():
    # define the function to submit the query
    def submit_query(query_entry, conn):
        query = query_entry.get("1.0", "end-1c")
        try:
            # Enable foreign key constraints
            conn.execute('PRAGMA foreign_keys = ON')

            conn.execute(query)
            conn.commit()
        except sqlite3.Error as e:
            messagebox.showerror("Error", e.args[0])
        except:
            messagebox.showerror("Error", "System error")
        else:
            messagebox.showinfo("Success", "Query submitted successfully")

    # Create a new window
    query_window = tk.Tk()
    query_window.title("Query By SQL")
    from main import setscreen
    setscreen(query_window, 800, 600)

    # Create a connection to the SQLite database
    conn = sqlite3.connect('hospital_database.db')

    # Create a space for the user to input his/her query
    query_label = tk.Label(query_window, text="Please input your query here:")
    query_label.pack(side=tk.TOP, padx=10, pady=15)
    query_entry = tk.Text(query_window, width=100, height=8)
    query_entry.pack(side=tk.TOP, padx=10, pady=15)

    # Create a button for the user to submit his/her query
    submit_button = tk.Button(query_window, text="submit", command=lambda: submit_query(query_entry, conn))
    submit_button.pack(side=tk.LEFT, padx=10, pady=15)

    # Create a button to exit the window
    exit_button = tk.Button(query_window, text="exit", command=lambda: query_window.destroy())
    exit_button.pack(side=tk.LEFT, padx=10, pady=15)


def save_rooms(entries):
    # Process the entered data (you can insert it into the database here)
    conn = sqlite3.connect('hospital_database.db')
    cursor = conn.cursor()
    room_ids = []

    try:
        for entry in entries:
            room_id = entry['room_id'].get()
            room_type = entry['room_type'].get()

            if room_id != "":
                if room_type in ("ICU", "normal"):
                    room_ids.append(room_id)
                    cursor.execute("PRAGMA foreign_keys = ON")
                    cursor.execute("INSERT INTO Rooms VALUES (?, ?)", (room_id, room_type))

        # Commit changes if no exceptions occurred
        conn.commit()

    except Exception as e:
        messagebox.showerror("Error", str(e))
        # Rollback changes in case of an exception
        conn.rollback()

    else:
        if len(room_ids) == 0:
            messagebox.showinfo("Info", "No new rooms inserted. Check if your entries are filled in correctly.")
        else:
            messagebox.showinfo("Success", f"New rooms inserted: {str(room_ids)}")

    finally:
        # Close the connection
        conn.close()


def add_entry(entries, frame):
    if len(entries) >= 5:
        messagebox.showwarning("Warning", "You can only add up to 5 entries at a time.")
        return
    # Create new Entry widgets for room_id and room_type
    entry = {'room_id': tk.Entry(frame), 'room_type': tk.Entry(frame)}

    # Add the new Entry widgets to the entries list
    entries.append(entry)

    # Place the Entry widgets in the grid
    row = len(entries) + 1
    entry['room_id'].grid(row=row, column=0, padx=5, pady=5)
    entry['room_type'].grid(row=row, column=1, padx=5, pady=5)


def add_rooms(main_window):
    main_window.destroy()

    view_window = tk.Tk()
    view_window.title("Confirm Doctor Table Info")

    from main import setscreen
    setscreen(view_window, 800, 600)

    # Create a frame to hold the Entry widgets
    entry_frame = tk.Frame(view_window)
    entry_frame.pack(padx=20, pady=20)

    # Create labels for room_id and room_type
    tk.Label(entry_frame, text="Room ID").grid(row=0, column=0, padx=5, pady=5)
    tk.Label(entry_frame, text="Room Type").grid(row=0, column=1, padx=5, pady=5)

    # Create a list to store Entry widgets
    entries = []

    # Add an initial entry
    add_entry(entries, entry_frame)

    button_frame = tk.Frame(view_window)
    button_frame.pack(pady=10)

    add_button = tk.Button(button_frame, text="Add Entry", command=lambda: add_entry(entries, entry_frame))
    add_button.pack(side="left", padx=(0, 30))

    save_button = tk.Button(button_frame, text="Save Entries", command=lambda: save_rooms(entries))
    save_button.pack(side="left", padx=(0, 30))

    exit_button = tk.Button(button_frame, text="Exit", command=lambda: exit_to_entry(view_window))
    exit_button.pack(side="left", ipadx=20)

    # Center the button frame within the view window
    view_window.update()
    button_frame.place(relx=0.5, rely=0.5, anchor="center")
    view_window.mainloop()


def logout(main_window):
    main_window.destroy()
    from main import create_login_window
    create_login_window()


def admin_application_entry_window():
    main_window = tk.Tk()
    main_window.title("Main Application")
    from main import setscreen
    setscreen(main_window, 600, 400)

    # Create four parallel buttons
    button1 = tk.Button(main_window, text="view table", command=lambda: view_tables(main_window))
    button2 = tk.Button(main_window, text="modify table", command=lambda: modify_tables_interface(main_window))
    button3 = tk.Button(main_window, text="confirm doctor info", command=lambda: confirm_doctors_info(main_window))
    button4 = tk.Button(main_window, text="confirm department info",
                        command=lambda: confirm_departments_info(main_window))
    button5 = tk.Button(main_window, text="query by SQL", command=query_by_SQL)
    button6 = tk.Button(main_window, text="add rooms", command=lambda: add_rooms(main_window))
    button7 = tk.Button(main_window, text="logout", command=lambda: logout(main_window))

    # Place the buttons two in a row
    button1.grid(row=0, column=1, padx=20, pady=15, sticky="ew")
    button2.grid(row=0, column=3, pady=15, sticky="ew")
    button3.grid(row=1, column=1, padx=20, pady=15, sticky="ew")
    button4.grid(row=1, column=3, pady=15, sticky="ew")
    button5.grid(row=2, column=1, padx=20, pady=15, sticky="ew")
    button6.grid(row=2, column=3, pady=15, sticky="ew")
    button7.grid(row=3, column=2, sticky="ew")

    main_window.grid_rowconfigure(0, weight=1)
    main_window.grid_rowconfigure(1, weight=1)
    main_window.grid_rowconfigure(2, weight=1)
    main_window.grid_rowconfigure(3, weight=1)
    main_window.grid_columnconfigure(0, weight=1)
    main_window.grid_columnconfigure(1, weight=3)
    main_window.grid_columnconfigure(2, weight=2)
    main_window.grid_columnconfigure(3, weight=3)
    main_window.grid_columnconfigure(4, weight=2)

    main_window.mainloop()
