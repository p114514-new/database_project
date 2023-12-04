import tkinter as tk
import tkinter.ttk as ttk
from tkinter.ttk import Treeview
from tkinter import scrolledtext
import sqlite3
import pandas as pd


username = 0
def doctor_application_entry_window(realnames, usernamepar):
    global realname
    global username
    username = usernamepar
    realname = realnames
    root = tk.Tk()
    root.title("Main Application")
    from main import setscreen
    setscreen(root, 400, 400)

    def fetch_data(realname):
        try:
            conn = sqlite3.connect('hospital_database.db')
            cursor = conn.cursor()

            cursor.execute(f"SELECT * FROM Doctors WHERE doctor_name='{realname}'")
            doctors_data = cursor.fetchall()
            print("Doctors data:")
            for row in doctors_data:
                print(row)

            cursor.execute(
                f"SELECT * FROM Treatments WHERE doctor_id IN (SELECT doctor_id FROM Doctors WHERE doctor_name='{realname}')")
            treatment_data = cursor.fetchall()
            print("Treatment data:")
            for row in treatment_data:
                print(row)

            conn.close()

            return doctors_data, treatment_data
        except sqlite3.Error as e:
            print(e)

    def display_data(textbox, data):
        textbox.delete('1.0', tk.END)
        if len(data) == 1:  # 如果只有一行数据
            for attribute in data[0]:
                textbox.insert(tk.INSERT, str(attribute) + '\n')
        else:  # 如果有多行数据
            for row in data:
                textbox.insert(tk.INSERT, ' | '.join(map(str, row)) + '\n')

    def refresh_data(realname, text_area_doctors):
        doctors_data, treatment_data = fetch_data(realname)

        text_area_doctors.delete('1.0', tk.END)
        for row in doctors_data:
            text_area_doctors.insert(tk.INSERT, ' | '.join(map(str, row)) + '\n')

    def open_update_window(realname, doctors_data):
        update_window = tk.Toplevel()

        tk.Label(update_window, text="Doctor ID").grid(column=0, row=1)
        doctor_id_entry = tk.Entry(update_window)
        doctor_id_entry.insert(0, doctors_data[0][0])
        doctor_id_entry.grid(column=0, row=0)

        tk.Label(update_window, text="Doctor Name").grid(column=1, row=1)
        doctor_name_entry = tk.Entry(update_window)
        doctor_name_entry.insert(0, doctors_data[0][1])
        doctor_name_entry.grid(column=1, row=0)

        tk.Label(update_window, text="Department ID").grid(column=2, row=1)
        department_id_entry = tk.Entry(update_window)
        department_id_entry.insert(0, doctors_data[0][2])
        department_id_entry.grid(column=2, row=0)

        update_button = tk.Button(update_window, text="Update",
                                  command=lambda: update_data(realname, doctor_id_entry.get(), doctor_name_entry.get(),
                                                              department_id_entry.get()))

        update_button.grid(column=1, row=3)

        def update_data(realname, doctor_id, doctor_name, department_id):
            print(doctor_id, doctor_name)
            # 验证doctor_id，doctor_name和department_id是否为空
            if not doctor_id or not doctor_name or not department_id:
                print("Error: doctor_id, doctor_name and department_id cannot be empty.")
                return

            # 验证doctor_id和department_id是否为数字
            if not doctor_id.isdigit() or not department_id.isdigit():
                print("Error: doctor_id and department_id must be numbers.")
                return

            # 验证doctor_name是否只包含字母和空格
            if not doctor_name.replace(' ', '').isalpha():
                print("Error: doctor_name must only contain letters and spaces.")
                return

            conn = sqlite3.connect('hospital_database.db')
            cursor = conn.cursor()
            doctors_data, treatment_data = fetch_data(realname)
            print(doctors_data)
            change_doctor_id = True if doctor_id != doctors_data[0][0] else False
            change_doctor_name = True if doctor_name != doctors_data[0][1] else False

            if change_doctor_id:
                cursor.execute(f"UPDATE Doctors SET doctor_id='{doctor_id}' WHERE doctor_id='{doctors_data[0][0]}'")
                cursor.execute(f"UPDATE Treatments SET doctor_id='{doctor_id}' WHERE doctor_id='{doctors_data[0][0]}'")
            if change_doctor_name:
                cursor.execute(f"UPDATE Doctors SET doctor_name='{doctor_name}' WHERE doctor_name='{doctors_data[0][1]}'")
                cursor.execute(
                    f"UPDATE Login SET realname='{doctor_name}' WHERE realname='{doctors_data[0][1]}' AND access_level=2")

            conn.commit()
            conn.close()

    def personal_info_window(realname):
        root.withdraw()
        personal_info = tk.Toplevel()
        personal_info.title("Personal Information")
        personal_info.geometry("500x500")  # 设置窗口大小为 500x500

        doctors_data, treatment_data = fetch_data(realname)

        tree = ttk.Treeview(personal_info)
        tree["columns"] = ("one", "two", "three", "four")
        tree.column("#0", width=125, minwidth=125, stretch=tk.NO)  # 调整列的宽度
        tree.column("one", width=125, minwidth=125, stretch=tk.NO)
        tree.column("two", width=125, minwidth=125)
        tree.column("three", width=125, minwidth=125, stretch=tk.NO)
        tree.column("four", width=125, minwidth=125, stretch=tk.NO)

        tree.heading("#0", text="Doctor ID", anchor=tk.W)
        tree.heading("one", text="Doctor Name", anchor=tk.W)
        tree.heading("two", text="Department ID", anchor=tk.W)
        tree.heading("three", text="Username", anchor=tk.W)

        for row in doctors_data:
            tree.insert("", 0, text=row[0], values=(row[1], row[2], row[3]))

        tree.pack(side='top', fill='both', expand=True)  # 让 Treeview 填充整个窗口

        update_button = tk.Button(personal_info, text="Update Information",
                                  command=lambda: open_update_window(realname, doctors_data))
        update_button.pack(side='top')

        refresh_button = tk.Button(personal_info, text="Refresh",
                                   command=lambda: refresh_info(personal_info, realname))
        refresh_button.pack(side='top')


        def refresh_info(personal_info, realname):
            personal_info.destroy()
            personal_info_window(realname)

        def back_to_main():
            personal_info.destroy()
            root.deiconify()  # 显示一级界面

        back_button = tk.Button(personal_info, text="Back", command=back_to_main)
        back_button.pack(side='bottom')

    def logout():
        root.destroy()
        from main import create_login_window
        create_login_window()

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


    def workbench_window(main_window, realname):
        main_window.destroy()
        workbench_interface = tk.Tk()
        workbench_interface.title("Workbench")
        from main import setscreen
        setscreen(workbench_interface, 800, 600)

        # Create a connection to the SQLite database
        conn = sqlite3.connect('hospital_database.db')
        cursor = conn.cursor()

        # Retrieve the available tables from the database schema
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = cursor.fetchall()
        conn.close()


        options = ['Patients', 'Doctors', 'Treatments']


        # Create a search module
        search_frame = tk.Frame(workbench_interface)
        name_for_search_frame = {'Patients': 'Patient Name', 'Doctors': 'Doctor Name', 'Treatments': 'Patient id'}
        search_column = {'Patients': 'patient_name', 'Doctors': 'doctor_name', 'Treatments': 'patient_id'}
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
        treeview = tk.ttk.Treeview(workbench_interface)

        # Create a label for displaying messages
        message_label = tk.Label(workbench_interface)

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
                treeview = tk.ttk.Treeview(workbench_interface)

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
        selected_table = tk.StringVar(workbench_interface)
        selected_table.set(options[0])
        option_menu = tk.OptionMenu(workbench_interface, selected_table, *options, command=on_selection_changed)
        option_menu.pack()

        # Execute the initial selection change to display the default table data
        on_selection_changed(selected_table.get())

        exit_button = tk.Button(workbench_interface, text="exit", command=lambda: exit_to_entry(workbench_interface))

        exit_button.pack(side=tk.BOTTOM)

        workbench_interface.mainloop()

        # 输入框和按钮
        tk.Label(workbench_interface, text="Patient Name").grid(column=0, row=1)
        patient_name_entry = tk.Entry(workbench_interface)
        patient_name_entry.grid(column=1, row=1)

        def search_patient(name):
            cursor.execute(f"SELECT * FROM Patients WHERE patient_name='{name}'")

            patient_data = cursor.fetchall()

            for i in tree_patients.get_children():
                tree_patients.delete(i)

            for row in patient_data:
                tree_patients.insert("", 0, text=row[0],
                                     values=(row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8]))

        search_button = tk.Button(workbench_interface, text="Search",
                                  command=lambda: search_patient(patient_name_entry.get()))
        search_button.grid(column=2, row=1)

        restore_button = tk.Button(workbench_interface, text="Restore",
                                   command=restore_patient)
        restore_button.grid(column=3, row=1)

        def refresh_data_workbench():
            restore_patient()

            doctors_data, treatment_data = fetch_data(realname)

            for i in tree_treatments.get_children():
                tree_treatments.delete(i)

            for row in treatment_data:
                tree_treatments.insert("", 0, text=row[0], values=(row[1], row[2], row[3], row[4], row[5]))

        refresh_button = tk.Button(workbench_interface, text="Refresh",
                                   command=refresh_data_workbench)
        refresh_button.grid(column=4, row=1)



    personal_info_button = tk.Button(root, text="Personal Information", command=lambda: personal_info_window(realname))
    personal_info_button.place(x=140, y=100)
    #personal_info_button.pack()

    workbench_button = tk.Button(root, text="Workbench", command=lambda: workbench_window(root, realname))
    workbench_button.place(x=165, y=200)
    #workbench_button.pack()

    logout_button = tk.Button(root, text="Logout", command=logout)  # 添加Logout按钮
    logout_button.place(x=175, y=300)
    #logout_button.pack()

    root.mainloop()
