import tkinter as tk
import tkinter.ttk as ttk
import sqlite3
import pandas as pd
from tkinter import messagebox
import tkinter.simpledialog as simpledialog
from collections import defaultdict


doctor_id = 0
doctor_name = 0
doctor_department_id = 0
username = 0

# def exit_to_entry(window):
#     window.destroy()
#     doctor_application_entry_window()

def exit_to_entry(window):
    window.destroy()
    doctor_application_entry_window_with_info()


def logout(main_window):
    main_window.destroy()
    from main import create_login_window
    create_login_window()


def Modify_self_info(main_window):
    main_window.destroy()
    modify_window = tk.Tk()
    modify_window.title("modification")
    from main import setscreen
    setscreen(modify_window, 800, 600)
    label_name = tk.Label(modify_window, text="name:")
    label_name.place(x=120, y=150)
    entry_name = tk.Entry(modify_window, width=30)
    entry_name.place(x=220, y=150)
    label_id = tk.Label(modify_window, text="id:")
    label_id.place(x=120, y=250)
    entry_id = tk.Entry(modify_window, width=30)
    entry_id.place(x=220, y=250)

    def modify_info():
        global doctor_id, doctor_name
        try:
            name = entry_name.get()
            id = int(entry_id.get())
            print(name, id)
            if name == '' or id == '':
                messagebox.showerror("Error", 'please fill the blanks')
            elif name.isalpha() != True:
                messagebox.showerror("Error", "Invalid Input for name")
                return False
            else:
                print(doctor_id)
                conn = sqlite3.connect('hospital_database.db')
                cursor = conn.cursor()
                conn.execute('PRAGMA foreign_keys = ON')

                cursor.execute("UPDATE Doctors SET doctor_id=?,doctor_name=? WHERE doctor_id = ?;",
                               (id, name, doctor_id))

                cursor.execute("UPDATE Login SET realname=? WHERE username = ?;", (name, username))

                conn.commit()
                messagebox.showinfo("Successful", "success!")
                doctor_name = name
                doctor_id = id
                conn.close()
        except Exception as e:
            messagebox.showerror("Error", e.args[0])

    button2 = tk.Button(modify_window, text=" Modify!",
                        command=lambda: modify_info())
    button5 = tk.Button(modify_window, text="Exit", command=lambda: exit_to_entry(modify_window))
    # Place the buttons vertically
    button2.pack(side=tk.TOP, padx=10, pady=15)
    button2.place(x=220, y=300)
    button5.pack(side=tk.TOP, padx=10, pady=15)
    button5.place(x=220, y=350)
    modify_window.mainloop()


def self_info(main_window):
    main_window.destroy()
    view_window = tk.Tk()
    view_window.title("View Table")
    from main import setscreen
    setscreen(view_window, 800, 600)
    # Create a connection to the SQLite database
    conn = sqlite3.connect('hospital_database.db')
    cursor = conn.cursor()

    res = cursor.execute("select * from Doctors where Doctors.username=?", (username,))

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

    update_button = tk.Button(view_window, text="update", command=lambda: Modify_self_info(view_window))
    update_button.pack(side=tk.BOTTOM)

    refresh_button = tk.Button(view_window, text="refresh", command=lambda: refresh_self_info())
    refresh_button.pack(side=tk.BOTTOM)



    def refresh_self_info():
        # Create a connection to the SQLite database
        conn = sqlite3.connect('hospital_database.db')
        cursor = conn.cursor()

        res = cursor.execute("select * from Doctors where Doctors.username=?", (username,))

        table_data = res.fetchall()
        conn.close()

        if table_data:
            # Create a pandas DataFrame from the table data
            df = pd.DataFrame(table_data)
            df.columns = [description[0] for description in cursor.description]

            # Destroy and recreate the columns in the Treeview widget
            treeview.delete(*treeview.get_children())

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

    view_window.mainloop()


def search_views(treeview, table, search_entry, search_column):
    conn = sqlite3.connect('hospital_database.db')
    cursor = conn.cursor()

    name = search_entry.get().strip()  # Get the entered doctor's name

    print(table, name, search_column)
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


def get_attributes():
    # query to get all table names
    conn = sqlite3.connect('hospital_database.db')
    cursor = conn.cursor()
    tables = ['Patients', 'Treatments']
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


def prompt_for_value(old_value):
    new_value = simpledialog.askstring("Modify Value", "Enter the new value:", initialvalue=old_value)
    return new_value


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
    elif column_name == 'access_level':
        return 3
    else:
        return 0

def is_valid_value(column_name, new_value):
    # Implement the logic to check if the new value is valid for the column
    # Replace with your own implementation
    pass
    return True

def update_value(treeview, values, new_value, table_name, column_name, primary_keys, cell_value):
    conn = sqlite3.connect('hospital_database.db')
    cursor = conn.cursor()

    # Check if the column is a primary key
    if is_key(table_name, column_name, primary_keys) == 1:
        messagebox.showwarning("Invalid Operation", "Modifying primary keys is not allowed.")
        return
    elif is_key(table_name, column_name, primary_keys) == 2:
        # list the appearance of the foreign key in all tables
        column_names = get_attributes()
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
    elif is_key(table_name, column_name, primary_keys) == 3:
        if int(new_value) == 4:
            messagebox.showwarning("Invalid Operation", "Modifying non-admin account to admin is not allowed.")
            return
        if int(cell_value) == 4:
            messagebox.showwarning("Invalid Operation", "You are cancelling your admin position.")
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
        print(query, (new_value, *primary_key_values))
        conn.commit()
        messagebox.showinfo("Value Updated", "The value has been successfully updated.")
    except sqlite3.Error as e:
        messagebox.showerror("Database Error", str(e))
    finally:
        conn.close()

    # Refresh the Treeview widget
    refresh_treeview(treeview, table_name)




def SelectItem(event, treeview, table_name):
    print(get_attributes())
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
    primary_keys = {'Patients': ['patient_id'], 'Treatments': ['treatment_id']}

    if new_value is not None:
        update_value(treeview, curItem['values'], new_value, table_name, column_name, primary_keys, cell_value)




def workbench(main_window):
    main_window.destroy()
    modifying_interface = tk.Tk()
    modifying_interface.title("Modify Table")
    from main import setscreen
    setscreen(modifying_interface, 800, 600)

    tables = [('Treatments',), ('Patients',)]
    # Remove the buffer tables from the options list
    options = [table[0] for table in tables if table[0] not in ["Buffer1", "Buffer2"]]
    print(tables)
    # Create a search module
    search_frame = tk.Frame(modifying_interface)
    name_for_search_frame = {'Patients': 'Patient Name', 'Treatments': 'Patient id'}
    search_column = {'Patients': 'patient_name', 'Treatments': 'patient_id'}
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


def doctor_application_entry_window_with_info():
    main_window = tk.Tk()
    main_window.title("Main Application")
    from main import setscreen
    setscreen(main_window, 600, 400)
    global doctor_id
    conn = sqlite3.connect('hospital_database.db')
    cursor = conn.cursor()
    t = cursor.execute("SELECT doctor_id from Doctors where username=?;", (username,))
    id = t.fetchall()
    doctor_id = id[0][0]
    # Create four parallel buttons

    button2 = tk.Button(main_window, text="self info", command=lambda: self_info(main_window))
    button4 = tk.Button(main_window, text="Workbench", command=lambda: workbench(main_window))
    button6 = tk.Button(main_window, text="logout", command=lambda: logout(main_window))

    # Place the buttons vertically

    button2.pack(side=tk.TOP, padx=10, pady=15)
    button4.pack(side=tk.TOP, padx=10, pady=15)
    button6.pack(side=tk.TOP, padx=10, pady=15)
    main_window.mainloop()


def doctor_application_entry_window(realname, usernamepar):
    global doctor_id
    global doctor_name
    global doctor_department_id
    global username
    username = usernamepar
    nurse_name = realname
    main_window = tk.Tk()
    main_window.title("Main Application")
    from main import setscreen
    setscreen(main_window, 600, 400)

    conn = sqlite3.connect('hospital_database.db')

    c = conn.cursor()

    try:
        # Enable foreign key constraints
        cursor = c.execute("select username  from Doctors where Doctors.username=?", (username,))
        conn.commit()
        result = cursor.fetchall()
        print(result, 'ok')
        if result:
            try:
                c.close()
                exit_to_entry(main_window)

            except sqlite3.Error as e:
                messagebox.showerror("Error", e.args[0])
        else:
            # Set window size to 600x400

            # Create the new realname label and entry
            label_nurse_id = tk.Label(main_window, text="nurse_id :")
            label_nurse_id.place(x=120, y=150)
            entry_nurse_id = tk.Entry(main_window, width=30)
            entry_nurse_id.place(x=220, y=150)

            label_nurse_gender = tk.Label(main_window, text="gender :")
            label_nurse_gender.place(x=120, y=200)
            entry_nurse_gender = tk.Entry(main_window, width=30)
            entry_nurse_gender.place(x=220, y=200)

            # Create a connection to the SQLite database
            def checkAccount():
                nurse_id = entry_nurse_id.get()
                nurse_gender = entry_nurse_gender.get()
                if nurse_gender != 'male' and nurse_gender != 'female':
                    messagebox.showerror("Error", "Invalid Input for gender")
                    return False
                try:
                    nurse_id = int(nurse_id)
                except ValueError:
                    messagebox.showerror("Error", "Invalid Input")
                    return False
                conn = sqlite3.connect('hospital_database.db')
                c = conn.cursor()
                try:
                    # Enable foreign key constraints
                    cursor = c.execute("select nurse_id,nurse_name,gender  from Nurses where Nurses.username=?",
                                       (username,))
                    conn.commit()
                    result = cursor.fetchall()
                    print(result)
                    if not result:
                        try:
                            c.execute("INSERT INTO Nurses VALUES (?,?,?,?)",
                                      (nurse_id, realname, nurse_gender, username))
                            conn.commit()
                            c.close()
                            exit_to_entry(main_window)

                        except sqlite3.Error as e:
                            messagebox.showerror("Error", e.args[0])
                    else:
                        messagebox.showerror("Error", "Id has already existed")
                        c.close()

                except sqlite3.Error as e:
                    messagebox.showerror("Error", e.args[0])
                except Exception as ee:
                    messagebox.showerror("Error", ee.args[0])

            # Create four parallel buttons
            button1 = tk.Button(main_window, text="ok", command=lambda: checkAccount())
            button2 = tk.Button(main_window, text="exit", command=lambda: logout(main_window))
            # Place the buttons vertically
            button1.pack(side=tk.TOP, padx=10, pady=15)
            button2.pack(side=tk.TOP, padx=10, pady=15)
            button1.place(x=150, y=250)
            button2.place(x=150, y=300)
            main_window.mainloop()
    except sqlite3.Error as e:
        messagebox.showerror("Error", e.args[0])
    except Exception as ee:
        messagebox.showerror("Error", ee.args[0])
