import datetime
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
            answer = messagebox.askquestion("Confirm", "Are you sure to approve the selected row(s)?\n" +
                                            "This operation cannot be undone.", icon='warning', type='yesno')
            if answer == 'no':
                return

            for row in selected_data:
                doctor_id = row[0]

                # delete the row in buffer1
                cursor.execute("DELETE FROM Buffer1 WHERE doctor_id = ?", (doctor_id,))

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


def deny_buffer_1(treeview):
    selected_items = treeview.selection()  # Get the selected items

    if selected_items:
        selected_lines = [int(x[1:]) - 1 for x in selected_items]
        selected_data = get_row_data(treeview, selected_lines)

        # Create a connection to the SQLite database
        conn = sqlite3.connect('hospital_database.db')
        cursor = conn.cursor()

        try:
            answer = messagebox.showinfo("Deny", "Are you sure to deny the selected row(s)?\n" +
                                         "This operation cannot be undone.", icon='warning', type='yesno')
            if answer == 'no':
                return

            for row in selected_data:
                doctor_id = row[0]

                # delete the row in buffer1
                cursor.execute("DELETE FROM Buffer1 WHERE doctor_id = ?", (doctor_id,))

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


def add_department_entry(entries, entry_frame):
    if len(entries) >= 10:
        messagebox.showwarning("Warning", "You can only add up to 10 entries at a time.")
        return
    # Create new Entry widgets for room_id and room_type
    entry = {'department_id': tk.Entry(entry_frame), 'department_name': tk.Entry(entry_frame)}

    entry['department_name'].config(width=30)

    # Add the new Entry widgets to the entries list
    entries.append(entry)

    # Place the Entry widgets in the grid
    row = len(entries) + 1
    entry['department_id'].grid(row=row, column=0, padx=5, pady=5)
    entry['department_name'].grid(row=row, column=1, padx=5, pady=5)


def save_departments(entries):
    # Process the entered data (you can insert it into the database here)
    conn = sqlite3.connect('hospital_database.db')
    cursor = conn.cursor()
    department_ids = []

    try:
        for entry in entries:
            department_id = entry['department_id'].get()
            department_name = entry['department_name'].get()

            if len(department_id) != 0:
                department_id = int(department_id.strip())
            if department_name:
                department_ids.append(department_id)
                cursor.execute("INSERT INTO Departments VALUES (?, ?)", (department_id, department_name))

        # Commit changes if no exceptions occurred
        conn.commit()

    except Exception as e:
        messagebox.showerror("Error", str(e))
        # Rollback changes in case of an exception
        conn.rollback()

    else:
        if len(department_ids) == 0:
            messagebox.showinfo("Info", "No new departments inserted. Check if your entries are filled in correctly.")
        else:
            messagebox.showinfo("Success", f"New departments inserted: {str(department_ids)}")

    finally:
        # Close the connection
        conn.close()


def add_new_department(main_window):
    main_window.destroy()
    add_department_window = tk.Tk()
    add_department_window.title("Add New Department")
    from main import setscreen
    setscreen(add_department_window, 800, 600)

    # similar as add_rooms
    # Create a frame to hold the Entry widgets
    entry_frame = tk.Frame(add_department_window)
    entry_frame.pack(padx=20, pady=20)

    # Create labels for room_id and room_type
    tk.Label(entry_frame, text="Department ID", ).grid(row=0, column=0, padx=5, pady=5)
    tk.Label(entry_frame, text="Department Name").grid(row=0, column=1, padx=5, pady=5)

    # Create a list to store Entry widgets
    entries = []

    # Add an initial entry
    add_department_entry(entries, entry_frame)

    button_frame = tk.Frame(add_department_window)
    button_frame.pack(pady=10)

    add_button = tk.Button(button_frame, text="Add Entry", command=lambda: add_department_entry(entries, entry_frame))
    add_button.pack(side="left", padx=(0, 30))

    save_button = tk.Button(button_frame, text="Save Entries", command=lambda: save_departments(entries))
    save_button.pack(side="left", padx=(0, 30))

    exit_button = tk.Button(button_frame, text="Exit", command=lambda: exit_to_entry(add_department_window))
    exit_button.pack(side="left", ipadx=20)

    # Center the button frame within the view window
    add_department_window.update()
    button_frame.place(relx=0.5, rely=0.8, anchor="center")
    add_department_window.mainloop()


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
    option_menu.pack(pady=10)

    # Execute the initial selection change to display the default table data
    on_selection_changed(selected_table.get())

    exit_button = tk.Button(view_window, text="exit", command=lambda: exit_to_entry(view_window))

    exit_button.pack(side=tk.BOTTOM, ipadx=20, ipady=5, padx=10, pady=10)

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
                    'Login': ['username']
                    }

    if new_value is not None:
        update_value(treeview, curItem['values'], new_value, table_name, column_name, primary_keys, cell_value)


def prompt_for_value(old_value):
    new_value = simpledialog.askstring("Modify Value", "Enter the new value:", initialvalue=old_value)
    return new_value


def update_value(treeview, values, new_value, table_name, column_name, primary_keys, cell_value):
    conn = sqlite3.connect('hospital_database.db')
    cursor = conn.cursor()
    column_names = get_all_attributes()

    # Check if the column is a primary key
    if is_key(table_name, column_name, primary_keys) == 1:
        messagebox.showwarning("Invalid Operation", "Modifying primary keys is not allowed.")
        return
    elif is_key(table_name, column_name, primary_keys) == 2:
        # list the appearance of the foreign key in all tables
        tables_having_this_key = [x for x in column_names if
                                  column_name in column_names[x] and x not in ['Buffer1', 'Buffer2']]
        if column_name in ['patient_name', 'nurse_name', 'staff_name', 'doctor_name', 'realname']:
            tables_having_this_key = ['Patients', 'Nurses', 'Hospital_Staff', 'Doctors', 'Login']
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
    elif is_key(table_name, column_name, primary_keys) == 3:
        if int(new_value) == 4:
            messagebox.showwarning("Invalid Operation", "Modifying non-admin account to admin is not allowed.")
            return
        if int(cell_value) == 4:
            messagebox.showwarning("Invalid Operation", "You are cancelling your admin position.")
            return

    # get the data type of the column
    query = f"PRAGMA table_info({table_name});"
    cursor.execute(query)
    attributes = cursor.fetchall()
    attributes = [attribute[2] for attribute in attributes]
    data_type = attributes[column_names[table_name].index(column_name)]

    # Check if the new value is valid
    if not is_valid_value(column_name, new_value, data_type):
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
        cursor.execute("PRAGMA foreign_keys = ON")
        cursor.execute(query, (new_value, *primary_key_values))
        print(query, (new_value, *primary_key_values))
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
    foreign_keys['Patients'] = ['room_id', 'patient_name', 'username']
    foreign_keys['Doctors'] = ['department_id', 'username']
    foreign_keys['Nurses'] = ['nurse_name', 'username']
    foreign_keys['Treatments'] = ['patient_id', 'doctor_id']
    foreign_keys['Nurse_Patient_Room'] = ['room_id', 'nurse_id', 'patient_id']
    foreign_keys['Hospital_Staff'] = ['staff_name', 'username']
    if column_name in primary_keys[table_name]:
        return 1
    elif column_name in foreign_keys[table_name]:
        return 2
    elif column_name == 'access_level':
        return 3
    else:
        return 0


def is_valid_value(column_name, new_value, data_type):
    if column_name == 'gender':
        if new_value.lower() in ['male', 'female']:
            return True
        else:
            return False

    if column_name == 'change_status':
        if new_value in ['+', '?', '-']:
            return True
        else:
            return False

    if new_value == '':
        return False

    if data_type == 'TEXT':
        return True

    if data_type == 'INTEGER':
        try:
            int(new_value)
            return True
        except ValueError:
            return False

    if data_type == 'REAL':
        try:
            float(new_value)
            return True
        except ValueError:
            return False

    if data_type == 'NUMERIC':
        try:
            float(new_value)
            return True
        except ValueError:
            return False

    if data_type == 'BOOLEAN':
        if new_value.lower() in ['true', 'false']:
            return True
        else:
            return False

    if data_type == 'DATE':
        try:
            datetime.datetime.strptime(new_value, '%Y-%m-%d')
            return True
        except ValueError:
            return False

    return True  # Assume any other data type is valid


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
    option_menu.pack(pady=10)

    # Execute the initial selection change to display the default table data
    on_selection_changed(selected_table.get())

    exit_button = tk.Button(modifying_interface, text="exit", command=lambda: exit_to_entry(modifying_interface))

    exit_button.pack(side=tk.BOTTOM, ipadx=20, ipady=5, padx=10, pady=10)

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

    button_frame = tk.Frame(view_window)
    button_frame.pack(pady=10)

    # Create buttons
    button1 = tk.Button(button_frame, text="Confirm", width=10, height=2, command=lambda: confirm_buffer_1(treeview))
    button2 = tk.Button(button_frame, text="Deny", width=10, height=2, command=lambda: deny_buffer_1(treeview))
    button3 = tk.Button(button_frame, text="exit", width=10, height=2, command=lambda: exit_to_entry(view_window))

    button1.pack(side=tk.LEFT, padx=10, pady=15)
    button2.pack(side=tk.LEFT, padx=10, pady=15)
    button3.pack(side=tk.LEFT, padx=10, pady=15)

    # Center the button frame within the view window
    view_window.update()
    button_frame.pack(anchor="center")

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


def query_by_SQL(main_window):
    # warn the user to not use this function if he/she does't have to
    result = messagebox.askquestion("Warning", "This function is only for advanced users. \n" +
                                    "You should not be using this function if you don't have to. \n" +
                                    "Please make sure you know what you are doing. \n" +
                                    "Do you want to continue? ",
                                    icon='warning',
                                    type='yesno')
    if result == 'no':
        return

    main_window.destroy()

    # Create a new window
    query_window = tk.Tk()
    query_window.title("Execute SQL Commands")
    from main import setscreen
    setscreen(query_window, 800, 600)

    # define the function to submit the query
    def submit_query(query_entry, conn):
        query = query_entry.get("1.0", "end-1c")
        try:
            cursor = conn.cursor()
            # Enable foreign key constraints
            cursor.execute('PRAGMA foreign_keys = ON')

            cursor.execute(query)

            # fetch the results if the query is a select query
            if query.lower().startswith("select"):
                search_results = cursor.fetchall()
                # use a messagebox to display the results
                messagebox.showinfo("Results", str(search_results))
            else:
                conn.commit()
        except sqlite3.Error as e:
            messagebox.showerror("Error", e.args[0])
        except Exception as e:
            messagebox.showerror("Error", str(e))
        else:
            if not query.lower().startswith("select"):
                messagebox.showinfo("Success", "Query submitted successfully")

    # Create a connection to the SQLite database
    conn = sqlite3.connect('hospital_database.db')

    # Create a space for the user to input his/her query
    query_label = tk.Label(query_window, text="Please input your command here:")
    query_label.pack(side=tk.TOP, padx=10, pady=15)
    query_entry = tk.Text(query_window, width=100, height=15)
    query_entry.pack(side=tk.TOP, padx=10, pady=15)

    button_frame = tk.Frame(query_window)
    button_frame.pack(pady=10)

    # Create a button for the user to submit his/her query
    submit_button = tk.Button(button_frame, text="submit", command=lambda: submit_query(query_entry, conn))
    submit_button.pack(side=tk.LEFT, padx=10, pady=15, ipadx=10, ipady=5)

    # Create a button to exit the window
    exit_button = tk.Button(button_frame, text="exit", command=lambda: exit_to_entry(query_window))
    exit_button.pack(side=tk.LEFT, padx=10, pady=15, ipadx=15, ipady=5)

    button_frame.pack(anchor="center")

    query_window.mainloop()


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


def add_room_entry(entries, frame):
    if len(entries) >= 10:
        messagebox.showwarning("Warning", "You can only add up to 10 entries at a time.")
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
    view_window.title("Add Rooms")

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
    add_room_entry(entries, entry_frame)

    button_frame = tk.Frame(view_window)
    button_frame.pack(pady=10)

    add_button = tk.Button(button_frame, text="Add Entry", command=lambda: add_room_entry(entries, entry_frame))
    add_button.pack(side="left", padx=(0, 30))

    save_button = tk.Button(button_frame, text="Save Entries", command=lambda: save_rooms(entries))
    save_button.pack(side="left", padx=(0, 30))

    exit_button = tk.Button(button_frame, text="Exit", command=lambda: exit_to_entry(view_window))
    exit_button.pack(side="left", ipadx=20)

    # Center the button frame within the view window
    view_window.update()
    button_frame.place(relx=0.5, rely=0.8, anchor="center")
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
    button4 = tk.Button(main_window, text="add new department",
                        command=lambda: add_new_department(main_window))
    button5 = tk.Button(main_window, text="query by SQL", command=lambda: query_by_SQL(main_window))
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
